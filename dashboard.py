# dashboard.py
# La interfaz de usuario para la Plataforma de Ciberseguridad Unificada.

import streamlit as st
import pandas as pd
import asyncio
import nest_asyncio

# Aplicamos el parche para permitir bucles de eventos anidados
nest_asyncio.apply()

# ¡CORREGIDO! Usamos la ruta a nuestro módulo
from modules.subdomain_finder import find_subdomains
from modules.validate import validate_subdomains_concurrently
# ¡CORREGIDO! Apuntamos a nuestro detector de tecnologías
from modules.tech_detector import detect_technologies 

st.set_page_config(page_title="Plataforma de Ciberseguridad", page_icon="🛡️", layout="wide")

# ... (El resto del código que proporcionaste es correcto y se puede pegar aquí tal cual) ...
# (Pega aquí el resto de tu código de dashboard.py)
def run_async_scan(func, data):
    """Helper para ejecutar cualquier función de escaneo asíncrona."""
    # Este helper es un poco simplificado, vamos a ajustarlo
    # para que maneje la lógica de nuestro tech_scanner que no es async
    if func.__name__ == 'validate_subdomains_concurrently':
        return asyncio.run(func(data))
    elif func.__name__ == 'detect_technologies':
        # Esta función no es async, así que la llamamos directamente
        # y procesamos la lista de subdominios.
        results = []
        for sub_data in data:
            tech = func(sub_data['url'])
            sub_data['technologies'] = tech
            results.append(sub_data)
        return results

# Initialize session state variables
if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None
if 'domain_scanned' not in st.session_state:
    st.session_state.domain_scanned = ""
if 'found_count' not in st.session_state:
    st.session_state.found_count = 0

st.title("🛡️ Plataforma de Ciberseguridad Unificada")
target_domain = st.text_input("Ingresa un dominio para analizar", placeholder="example.com")

if st.button("Iniciar Análisis"):
    if target_domain:
        st.session_state.scan_results = None

        with st.spinner("Fase 1/3: Descubriendo subdominios..."):
            # Usamos la ruta que ya tenemos configurada
            found_subdomains = find_subdomains(target_domain, "sublist3r/sublist3r.py")
        st.session_state.found_count = len(found_subdomains)
        if not found_subdomains:
            st.warning("No se descubrieron subdominios."); st.stop()

        with st.spinner(f"Fase 2/3: Validando {len(found_subdomains)} subdominios..."):
            active_subdomains = run_async_scan(validate_subdomains_concurrently, found_subdomains)
        if not active_subdomains:
            st.warning("No se encontraron sitios activos."); st.stop()

        with st.spinner(f"Fase 3/3: Detectando tecnologías en {len(active_subdomains)} sitios activos..."):
            results_with_tech = run_async_scan(detect_technologies, active_subdomains)

        st.session_state.scan_results = results_with_tech
        st.session_state.domain_scanned = target_domain
        st.success("¡Análisis de tecnología completado!")
        st.rerun()
    else:
        st.error("Por favor, ingresa un dominio para analizar.")

if st.session_state.scan_results is not None:
    results = st.session_state.scan_results
    domain = st.session_state.domain_scanned
    found_count = st.session_state.found_count

    st.subheader(f"Resultados para: {domain}")

    col1, col2 = st.columns(2)
    col1.metric("Subdominios Descubiertos", found_count)
    col2.metric("Sitios Activos Analizados", len(results))

    st.divider()

    st.write("#### Tabla de Tecnologías Detectadas")
    
    # Convertimos los resultados a un formato que Pandas pueda manejar
    display_data = []
    for item in results:
        tech_list = item.get('technologies')
        if tech_list:
            for tech in tech_list:
                display_data.append({
                    'Subdominio': item['subdomain'],
                    'URL': item['url'],
                    'Tecnología Detectada': tech['name']
                })
        else:
             display_data.append({
                    'Subdominio': item['subdomain'],
                    'URL': item['url'],
                    'Tecnología Detectada': 'N/A'
                })

    df_display = pd.DataFrame(display_data)

    st.dataframe(
            df_display, 
            use_container_width=True
        )