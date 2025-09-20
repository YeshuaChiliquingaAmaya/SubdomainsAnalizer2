# modules/discovery.py

import whois
from datetime import datetime

def get_domain_age(domain_name: str) -> float | None:
    """
    Calcula la antigüedad de un dominio en años.

    Args:
        domain_name (str): El nombre del dominio a consultar (ej: 'google.com').

    Returns:
        float | None: La antigüedad del dominio en años, o None si no se puede determinar.
    """
    try:
        domain_info = whois.whois(domain_name)
        
        # El resultado de creation_date puede ser una fecha o una lista de fechas.
        # Nos aseguramos de tomar la más antigua (la primera).
        creation_date = domain_info.creation_date
        if isinstance(creation_date, list):
            creation_date = creation_date[0]

        if creation_date:
            # Calculamos la diferencia entre hoy y la fecha de creación.
            age_delta = datetime.now() - creation_date
            # Convertimos la diferencia a años (aproximado).
            age_in_years = age_delta.days / 365.25
            return round(age_in_years, 2)
        else:
            return None
            
    except Exception as e:
        # Si el dominio no existe o hay un error en la consulta WHOIS.
        print(f"[-] Error al obtener la antigüedad de {domain_name}: {e}")
        return None

def get_subdomain_hierarchy(subdomain: str) -> int:
    """
    Calcula el nivel de jerarquía de un subdominio.

    Ej: 'google.com' -> 0
        'www.google.com' -> 1
        'docs.dev.google.com' -> 2

    Args:
        subdomain (str): El subdominio a analizar.

    Returns:
        int: El nivel de jerarquía.
    """
    # Quitamos 'http://' o 'https://' por si acaso.
    if subdomain.startswith(('http://', 'https://')):
        subdomain = subdomain.split('//')[1]
        
    parts = subdomain.split('.')
    # La jerarquía es el número de partes menos el dominio principal y el TLD (ej: 'google' y 'com').
    # Si hay 2 o menos partes, la jerarquía es 0.
    hierarchy_level = len(parts) - 2
    return max(0, hierarchy_level)

def get_discovery_info(target_domain: str) -> dict:
    """
    Función principal del módulo que orquesta el descubrimiento de información.

    Args:
        target_domain (str): El dominio o subdominio objetivo.

    Returns:
        dict: Un diccionario con la información recolectada.
    """
    print(f"[+] Iniciando descubrimiento para: {target_domain}")
    
    # Para la antigüedad, necesitamos el dominio raíz (ej: 'google.com' de 'www.google.com')
    parts = target_domain.split('.')
    root_domain = '.'.join(parts[-2:])

    age = get_domain_age(root_domain)
    hierarchy = get_subdomain_hierarchy(target_domain)
    
    discovery_data = {
        'domain': target_domain,
        'root_domain': root_domain,
        'age_in_years': age,
        'hierarchy_level': hierarchy
    }
    
    return discovery_data