# modules/risk_scorer.py

import socket
from concurrent.futures import ThreadPoolExecutor

def check_single_port(domain: str, port: int) -> int | None:
    """Intenta conectarse a un único puerto y devuelve el puerto si está abierto."""
    try:
        # Usamos un timeout corto para no esperar demasiado
        with socket.create_connection((domain, port), timeout=0.5):
            return port
    except (socket.timeout, ConnectionRefusedError):
        return None
    except Exception:
        return None

def check_open_ports(domain: str) -> list[int]:
    """
    Escanea una lista de puertos comunes para ver si están abiertos en un dominio.

    Args:
        domain (str): El dominio o subdominio a escanear.

    Returns:
        list[int]: Una lista de los puertos que se encontraron abiertos.
    """
    # Lista de puertos comunes que indican exposición
    common_ports = [21, 22, 23, 25, 80, 110, 143, 443, 445, 3306, 3389, 5900, 8080]
    open_ports = []
    
    print(f"[+] Escaneando puertos comunes en: {domain}")
    # Usamos múltiples hilos para hacer el escaneo mucho más rápido
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Creamos una tarea para cada puerto
        future_to_port = {executor.submit(check_single_port, domain, port): port for port in common_ports}
        for future in future_to_port:
            result = future.result()
            if result:
                open_ports.append(result)

    return open_ports

def calculate_hybrid_risk_score(discovery_data: dict, cve_data: list, open_ports: list) -> dict:
    """
    Calcula una puntuación de riesgo híbrida basada en múltiples factores.

    Args:
        discovery_data (dict): Datos del módulo de descubrimiento (antigüedad, jerarquía).
        cve_data (list): Lista de CVEs encontrados (actualmente simulados).
        open_ports (list): Lista de puertos abiertos.

    Returns:
        dict: Un diccionario con el puntaje final y el desglose.
    """
    score = 0
    breakdown = {}

    # --- Ponderaciones (pueden ser ajustadas) ---
    WEIGHT_AGE = 0.5
    WEIGHT_HIERARCHY = 2
    WEIGHT_CVSS = 5  # El factor más pesado
    WEIGHT_PORT = 10 # Penalización alta por cada puerto expuesto
    WEIGHT_PUBLIC = 5  # Penalización base por ser un activo público

    # 1. Factor: Antigüedad (más antiguo, más riesgo)
    age = discovery_data.get('age_in_years', 0)
    age_score = (age * WEIGHT_AGE) if age else 0
    score += age_score
    breakdown['Antigüedad'] = f"+{age_score:.2f} pts"

    # 2. Factor: Jerarquía (más complejo, más riesgo)
    hierarchy = discovery_data.get('hierarchy_level', 0)
    hierarchy_score = hierarchy * WEIGHT_HIERARCHY
    score += hierarchy_score
    breakdown['Jerarquía'] = f"+{hierarchy_score:.2f} pts"
    
    # 3. Factor: Puntuación CVSS (el más alto encontrado)
    max_cvss = 0
    if cve_data:
        for cve in cve_data:
            # Nos aseguramos de manejar puntajes 'N/A' o None
            if isinstance(cve.get('score'), (int, float)) and cve.get('score', 0) > max_cvss:
                max_cvss = cve['score']
    
    cvss_score = max_cvss * WEIGHT_CVSS
    score += cvss_score
    #breakdown['CVSS Máximo'] = f"+{cvss_score:.2f} pts (usando {max_cvss}) - ¡DATO SIMULADO!"

    # 4. Factor: Exposición por puertos abiertos
    port_score = len(open_ports) * WEIGHT_PORT
    score += port_score
    breakdown['Puertos Abiertos'] = f"+{port_score:.2f} pts (puertos: {open_ports})"

    # 5. Factor: Activo público (Frente al cliente)
    score += WEIGHT_PUBLIC
    breakdown['Activo Público'] = f"+{WEIGHT_PUBLIC:.2f} pts"

    # Normalizamos el puntaje a una escala de 0-100 para fácil interpretación
    # (Este máximo es una estimación, se puede ajustar)
    max_possible_score = 100 
    final_score = min(score, max_possible_score)

    return {'score': round(final_score, 2), 'breakdown': breakdown}