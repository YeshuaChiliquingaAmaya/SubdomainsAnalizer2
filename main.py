# main.py

# ¡NUEVO! Importamos asyncio para manejar la concurrencia.
import asyncio
import json
import os

from modules.discovery import get_discovery_info
from modules.tech_detector import detect_technologies
from modules.risk_scorer import calculate_hybrid_risk_score, check_open_ports
from modules.subdomain_finder import find_subdomains
# ¡NUEVO! Importamos nuestro módulo de validación.
from modules.validate import validate_subdomains_concurrently
from modules.ml_classifier import predict_risk_profile
from modules.report import generate_pdf_report

# --- CONFIGURACIÓN ---
ROOT_DOMAIN = "prowessec.com"
SUBDOMAIN_LIMIT = 0 # Ponemos 0 para analizar todos los subdominios activos encontrados
SUBLIST3R_PATH = "sublist3r/sublist3r.py"
# ---------------------

# ¡CAMBIO IMPORTANTE! La función principal ahora es 'async def'.
async def main():
    """
    Flujo principal del programa de análisis de seguridad.
    """
    # 1. Búsqueda inicial de subdominios
    potential_subdomains = find_subdomains(ROOT_DOMAIN, SUBLIST3R_PATH)
    
    if not potential_subdomains:
        print("[-] No se encontraron subdominios para analizar. Terminando el programa.")
        return

    # 2. ¡NUEVO PASO! Validación concurrente de subdominios
    # 'await' le dice a Python que espere a que esta tarea asíncrona termine.
    active_subdomains_data = await validate_subdomains_concurrently(potential_subdomains)

    if not active_subdomains_data:
        print("[-] No se encontraron subdominios activos. Terminando el programa.")
        return

    # Aplicamos el límite DESPUÉS de encontrar los subdominios activos
    if SUBDOMAIN_LIMIT > 0 and len(active_subdomains_data) > SUBDOMAIN_LIMIT:
        print(f"\n[!] Aplicando límite de {SUBDOMAIN_LIMIT} subdominios para el análisis.")
        subdomains_to_scan = active_subdomains_data[:SUBDOMAIN_LIMIT]
    else:
        subdomains_to_scan = active_subdomains_data

    # --- BUCLE PRINCIPAL DE ANÁLISIS ---
    # ¡CAMBIO! Ahora iteramos sobre la lista de diccionarios de subdominios activos.
    for sub_data in subdomains_to_scan:
        domain = sub_data['subdomain']
        url = sub_data['url'] # Ya sabemos la URL activa (http o https)

        print(f"\n\n=================================================")
        print(f"  Analizando Objetivo Activo: {domain} ({url})")
        print(f"=================================================")

        try:
            # Flujo de análisis que ya teníamos
            discovery_data = get_discovery_info(domain)
            # Usamos la URL activa que ya descubrimos
            tech_data = detect_technologies(url)
            mock_cve_data = [{'id': 'CVE-SIMULADO-ALTO', 'score': 9.8, 'summary': '...'}] if tech_data else []
            open_ports = check_open_ports(domain)
            risk_info = calculate_hybrid_risk_score(discovery_data, mock_cve_data, open_ports)
            risk_prediction = predict_risk_profile(risk_info['score'])
            
            # Impresión de Resultados
            print("\n--- Resultados de Detección de Tecnologías ---")
            if tech_data:
                print(json.dumps(tech_data, indent=2, ensure_ascii=False))
            else:
                print("No se detectaron tecnologías específicas.")

            print("\n--- Resultados de Puntuación de Riesgo ---")
            print(f"PUNTUACIÓN FINAL: {risk_info['score']} / 100")
            print(f"PERFIL ML PREDICHO: {risk_prediction}")
            print("Desglose:")
            print(json.dumps(risk_info['breakdown'], indent=2, ensure_ascii=False))
            
        except Exception as e:
            print(f"\n[-] Ocurrió un error al procesar el dominio {domain}: {e}")
            continue

# --- PASO FINAL: GENERACIÓN DE REPORTE ---
    if subdomains_to_scan:
        print("\n\n=================================================")
        print("          Generando Reporte Final")
        print("=================================================")
        
        # Generamos el nombre del archivo basado en el dominio
        report_filename = f"reporte_{ROOT_DOMAIN}.pdf"
        
        # Obtenemos los datos del PDF en memoria
        pdf_data = generate_pdf_report(ROOT_DOMAIN, subdomains_to_scan)
        
        # Guardamos los datos en un archivo
        with open(report_filename, "wb") as f:
            f.write(pdf_data)
        
        print(f"[+] Reporte guardado exitosamente como: {report_filename}")

if __name__ == "__main__":
    asyncio.run(main())