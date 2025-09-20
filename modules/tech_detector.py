# modules/tech_detector.py

# Ignoramos advertencias de Wappalyzer que no son críticas
import logging
logging.getLogger().setLevel(logging.ERROR)

from Wappalyzer import Wappalyzer, WebPage
import requests

def detect_technologies(url: str) -> list[dict] | None:
    """
    Detecta las tecnologías web utilizadas en una URL.

    Args:
        url (str): La URL a analizar (debe incluir http:// o https://).

    Returns:
        list[dict] | None: Una lista de diccionarios con las tecnologías y sus versiones,
                           o None si ocurre un error.
    """
    # Verificamos que la URL tenga el esquema http/https
    if not url.startswith(('http://', 'https://')):
        print(f"[-] URL inválida: {url}. Debe empezar con http:// o https://")
        return None

    try:
        # Hacemos una petición para obtener el contenido de la página
        response = requests.get(url, verify=False, timeout=10) # verify=False para ignorar errores SSL
        
        # Creamos un objeto WebPage con el contenido y las cabeceras
        webpage = WebPage(
            response.url,
            response.text,
            response.headers
        )
        
        # Inicializamos Wappalyzer y analizamos la página
        wappalyzer = Wappalyzer.latest()
        technologies_found = wappalyzer.analyze_with_versions(webpage)
        
        # Formateamos el resultado en una lista de diccionarios
        tech_list = []
        for tech, info in technologies_found.items():
            # 'versions' es una lista, tomamos la primera si existe
            version = info.get('versions')[0] if info.get('versions') else None
            tech_list.append({'name': tech, 'version': version})
            
        return tech_list

    except requests.RequestException as e:
        print(f"[-] Error de red al acceder a {url}: {e}")
        return None
    except Exception as e:
        print(f"[-] Ocurrió un error inesperado durante la detección de tecnologías: {e}")
        return None