# modules/deep_scanner.py
# Módulo para realizar un escaneo profundo de tecnologías.
# ✨ ¡VERSIÓN MODIFICADA! Ahora usa 'webtech' y es multiplataforma (Windows/Linux).

import requests
import webtech  # Reemplaza a 'subprocess' y 'json' para esta tarea

def deep_scan_technologies(url: str) -> list[dict]:
    """
    Usa la biblioteca 'webtech' para realizar un escaneo de tecnologías en una URL.
    Esta función es el reemplazo directo de la versión que usaba WhatWeb.
    """
    results = []
    
    try:
        # 1. Aseguramos que la URL tenga un esquema (http/https) para 'requests'.
        if not url.startswith(('http://', 'https://')):
            url = 'https://' + url

        # 2. Hacemos la petición web. Usamos verify=False para evitar errores SSL comunes
        #    en sitios de prueba y un User-Agent para simular un navegador.
        response = requests.get(
            url, 
            timeout=20, 
            verify=False,
            headers={'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'}
        )
        response.raise_for_status()  # Lanza un error si la respuesta es 4xx o 5xx

        # 3. Analizamos la respuesta con webtech.
        wt = webtech.WebTech()
        tech_report = wt.start_from_response(response)

        # 4. Transformamos la salida de webtech al formato que tu app espera: [{'name': ..., 'version': ...}]
        for tech_name, tech_info in tech_report.items():
            version = tech_info.get("version")  # Usamos .get() para evitar errores si no hay versión
            results.append({"name": tech_name, "version": version})

    except requests.exceptions.RequestException as e:
        # Captura errores de red (timeout, DNS, conexión rechazada, etc.)
        # print(f"[!] Error de red al escanear {url}: {e}") # Descomenta para depurar
        pass 
    except Exception as e:
        # Captura cualquier otro error inesperado.
        # print(f"[!] Error inesperado durante el escaneo de {url}: {e}") # Descomenta para depurar
        pass

    return results