# modules/validate.py
# Este módulo se encarga de verificar qué subdominios están activos y responden
# a peticiones HTTP.

import asyncio
import aiohttp

async def check_subdomain(session, subdomain):
    """
    Intenta conectarse a un subdominio a través de HTTP y HTTPS.
    Usa una petición HEAD para ser más rápido, ya que solo queremos el estado.
    """
    urls_to_try = [f"https://{subdomain}", f"http://{subdomain}"]

    for url in urls_to_try:
        try:
            async with session.head(url, timeout=5, allow_redirects=True) as response:
                if response.status < 400:
                    return {"subdomain": subdomain, "status": response.status, "url": str(response.url)}
        except (aiohttp.ClientError, asyncio.TimeoutError):
            continue
    return None

async def validate_subdomains_concurrently(subdomains):
    """
    Recibe una lista de subdominios y los verifica de forma concurrente.
    """
    print(f"\n[*] Iniciando validación de {len(subdomains)} subdominios...")
    active_subdomains = []

    async with aiohttp.ClientSession(headers={'User-Agent': 'Python-Security-Scanner'}) as session:
        tasks = [check_subdomain(session, sub) for sub in subdomains]
        results = await asyncio.gather(*tasks)
        active_subdomains = [res for res in results if res is not None]

    print(f"[+] Validación completada. Se encontraron {len(active_subdomains)} subdominios activos.")
    return active_subdomains