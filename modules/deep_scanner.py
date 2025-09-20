# modules/deep_scanner.py
# Módulo para realizar un escaneo profundo de tecnologías usando WhatWeb.

import subprocess
import json

def deep_scan_technologies(url: str) -> list[dict]:
    """
    Usa WhatWeb para realizar un escaneo profundo de una URL.
    """
    results = []
    try:
        command = ["whatweb", "--color=never", "--log-json=-", url]
        process = subprocess.run(
            command, 
            capture_output=True, 
            text=True, 
            check=True, 
            timeout=120
        )

        for line in process.stdout.strip().split('\n'):
            # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
            # Nos aseguramos de que la línea no esté vacía antes de procesarla
            # y la envolvemos en un try-except para ignorar las que no son JSON.
            if line:
                try:
                    data = json.loads(line)
                    if "plugins" in data:
                        for plugin_name, plugin_data in data["plugins"].items():
                            version = plugin_data.get("version", [None])[0]
                            results.append({"name": plugin_name, "version": version})
                except json.JSONDecodeError:
                    # Si una línea no es JSON (ej. un error de WhatWeb), la ignoramos.
                    # print(f"[!] Aviso: WhatWeb devolvió una línea no-JSON para {url}, ignorando.")
                    continue

    except FileNotFoundError:
        print("[!] Error: El comando 'whatweb' no fue encontrado. ¿Está instalado?")
    except subprocess.CalledProcessError as e:
        print(f"[!] Error ejecutando WhatWeb en {url}: {e.stderr}")
    except Exception as e:
        print(f"[!] Error inesperado durante el escaneo profundo de {url}: {e}")

    return results