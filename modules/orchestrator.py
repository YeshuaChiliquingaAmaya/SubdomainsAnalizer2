# modules/orchestrator.py (versión corregida y robusta)

import asyncio
from .tech_detector import detect_technologies
from .deep_scanner import deep_scan_technologies
from .content_discovery import discover_sensitive_paths

async def scan_single_target_tech(sub_data):
    url = sub_data['url']
    quick_tech_task = asyncio.to_thread(detect_technologies, url)
    deep_tech_task = asyncio.to_thread(deep_scan_technologies, url)
    quick_tech = await quick_tech_task or []
    deep_tech = await deep_tech_task or []
    combined_tech = {t['name']: t for t in quick_tech}
    combined_tech.update({t['name']: t for t in deep_tech})
    sub_data['technologies'] = list(combined_tech.values())
    return sub_data

async def run_full_tech_scan(active_subdomains):
    tasks = [scan_single_target_tech(sub) for sub in active_subdomains]
    results_with_tech = await asyncio.gather(*tasks)
    return results_with_tech

async def run_content_discovery_scan(active_subdomains):
    """
    Orquesta el escaneo de rutas sensibles para todos los subdominios de forma concurrente
    y maneja los errores de forma individual.
    """
    all_found_paths = {}
    
    async def discover_for_sub(sub_data):
        # Devolvemos el subdominio junto con el resultado para poder identificarlo
        paths = await discover_sensitive_paths(sub_data['url'], "wordlist.txt")
        return sub_data['subdomain'], paths

    # --- ¡AQUÍ ESTÁ LA CORRECCIÓN CLAVE! ---
    tasks = [discover_for_sub(sub) for sub in active_subdomains]
    # 'return_exceptions=True' evita que todo se detenga si una tarea falla.
    results = await asyncio.gather(*tasks, return_exceptions=True)
    
    for result in results:
        # Ahora revisamos cada resultado individualmente
        if isinstance(result, Exception):
            # Si el resultado es una excepción, la imprimimos para saber qué pasó.
            print(f"[!] Error en una de las tareas de descubrimiento de contenido: {result}")
        else:
            # Si el resultado es exitoso (una tupla de subdominio, paths)
            subdomain, paths_found = result
            if paths_found:
                all_found_paths[subdomain] = paths_found
                
    return all_found_paths