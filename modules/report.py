# report.py
# Módulo para generar reportes en PDF con la lista de subdominios activos.

from jinja2 import Environment, FileSystemLoader
from weasyprint import HTML
import datetime

def generate_pdf_report(domain, active_subdomains):
    """
    Genera un reporte en PDF con la lista de subdominios activos.

    Args:
        domain (str): El dominio que fue escaneado.
        active_subdomains (list): Lista de diccionarios de subdominios activos.

    Returns:
        bytes: El contenido del archivo PDF en bytes.
    """
    print("[*] Generando reporte en PDF...")
    
    env = Environment(loader=FileSystemLoader('.'))
    template = env.get_template("template.html")

    html_out = template.render(
        domain=domain,
        report_date=datetime.date.today().strftime("%d-%m-%Y"),
        results=active_subdomains
    )

    pdf_bytes = HTML(string=html_out).write_pdf()
    print("[+] Reporte PDF generado en memoria.")
    return pdf_bytes