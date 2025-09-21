# modules/content_discovery.py
# Descubre rutas, directorios y archivos sensibles en un dominio.

import asyncio
import aiohttp

async def check_path(session, base_url, path):
    """Verifica una única ruta y devuelve la URL si es encontrada."""
    url_to_try = f"{base_url.rstrip('/')}/{path.strip()}"
    try:
        # Usamos GET en lugar de HEAD porque algunos servidores no responden a HEAD
        async with session.get(url_to_try, timeout=5, allow_redirects=False) as response:
            # Nos interesan respuestas OK (200), Prohibido (403) o Redirecciones (301/302)
            if response.status in [200, 403, 301, 302]:
                return {"path": f"/{path}", "status": response.status, "url": url_to_try}
    except (aiohttp.ClientError, asyncio.TimeoutError):
        pass # Ignoramos errores de conexión y timeouts
    return None

async def discover_sensitive_paths(base_url: str, wordlist_path: str) -> list[dict]:
    """
    Lee un diccionario y prueba cada ruta en la URL base de forma concurrente.
    """
    found_paths = []
    try:
        with open(wordlist_path, "r") as f:
            wordlist = f.readlines()
    except FileNotFoundError:
        print(f"[!] Error: No se encontró el diccionario en '{wordlist_path}'")
        return []

    async with aiohttp.ClientSession(headers={'User-Agent': 'Python-Security-Scanner'}) as session:
        tasks = [check_path(session, base_url, path) for path in wordlist]
        results = await asyncio.gather(*tasks)
        found_paths = [res for res in results if res is not None]

    return found_paths