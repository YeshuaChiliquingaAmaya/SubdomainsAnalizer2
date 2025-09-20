# modules/orchestrator.py
# Orquesta los diferentes escaneos de tecnología de forma concurrente.

import asyncio
from .tech_detector import detect_technologies
from .deep_scanner import deep_scan_technologies

async def scan_single_target_tech(sub_data):
    """
    Ejecuta todos los escaneos de tecnología para un único objetivo.
    """
    url = sub_data['url']

    # 1. Escaneo rápido (Wappalyzer) - Es síncrono, lo ejecutamos en un hilo.
    quick_tech_task = asyncio.to_thread(detect_technologies, url)

    # 2. Escaneo profundo (WhatWeb) - Es síncrono, lo ejecutamos en otro hilo.
    deep_tech_task = asyncio.to_thread(deep_scan_technologies, url)

    # Esperamos a que ambos terminen
    quick_tech = await quick_tech_task or []
    deep_tech = await deep_tech_task or []

    # 3. Combinamos los resultados y eliminamos duplicados
    combined_tech = {t['name']: t for t in quick_tech}
    combined_tech.update({t['name']: t for t in deep_tech})

    sub_data['technologies'] = list(combined_tech.values())
    return sub_data

async def run_full_tech_scan(active_subdomains):
    """
    Orquesta el escaneo de tecnologías para una lista de subdominios activos.
    """
    # Creamos una tarea de escaneo para cada subdominio activo.
    tasks = [scan_single_target_tech(sub) for sub in active_subdomains]

    # asyncio.gather ejecuta todas las tareas de forma concurrente.
    results_with_tech = await asyncio.gather(*tasks)

    return results_with_tech