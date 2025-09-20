# modules/subdomain_finder.py
# Este módulo es responsable de encontrar subdominios usando la herramienta externa Sublist3r.

import subprocess
import sys
import os

def find_subdomains(domain, sublist3r_path):
    """
    Ejecuta Sublist3r para encontrar subdominios para un dominio dado.

    Args:
        domain (str): El dominio objetivo (ej. 'example.com').
        sublist3r_path (str): La ruta al script sublist3r.py.

    Returns:
        list: Una lista de subdominios encontrados, o una lista vacía si ocurre un error.
    """
    print(f"[*] Iniciando escaneo de Sublist3r para: {domain}")

    output_file = "subdomains.tmp"

    command = [
        sys.executable,
        sublist3r_path,
        "-d",
        domain,
        "-o",
        output_file
    ]

    try:
        subprocess.run(
            command, 
            check=True, 
            capture_output=True, 
            text=True, 
            timeout=600
        )

        with open(output_file, "r") as f:
            subdomains = sorted(list(set([line.strip() for line in f.readlines()])))

        os.remove(output_file)

        print(f"[+] Escaneo de Sublist3r completado. Se encontraron {len(subdomains)} subdominios.")
        return subdomains

    except FileNotFoundError:
        print(f"[!] Error: No se encontró el script de Sublist3r en '{sublist3r_path}'.")
        print("[!] Verifica la ruta en main.py.")
        return []
    except subprocess.CalledProcessError as e:
        print(f"[!] Error al ejecutar Sublist3r. Es posible que una de sus dependencias haya fallado.")
        print(f"[!] Error details: {e.stderr}")
        return []
    except subprocess.TimeoutExpired:
        print("[!] Error: El escaneo de Sublist3r tardó demasiado y fue cancelado (timeout).")
        return []
    except Exception as e:
        print(f"[!] Ocurrió un error inesperado: {e}")
        return []