# dashboard.py (versión corregida)

import streamlit as st
import pandas as pd
import asyncio
import nest_asyncio

nest_asyncio.apply()

from modules.subdomain_finder import find_subdomains
from modules.validate import validate_subdomains_concurrently
from modules.orchestrator import run_full_tech_scan

st.set_page_config(page_title="Plataforma de Ciberseguridad", page_icon="🛡️", layout="wide")

def run_async_function(func, *args):
    return asyncio.run(func(*args))

if 'scan_results' not in st.session_state:
    st.session_state.scan_results = None
if 'domain_scanned' not in st.session_state:
    st.session_state.domain_scanned = ""
if 'found_count' not in st.session_state:
    st.session_state.found_count = 0

st.title("🛡️ Plataforma de Ciberseguridad Unificada")
target_domain = st.text_input("Ingresa un dominio para analizar", placeholder="prowessec.com")

if st.button("Iniciar Análisis Profundo"):
    if target_domain:
        st.session_state.scan_results = None
        with st.spinner("Fase 1/3: Descubriendo subdominios (Sublist3r)..."):
            found_subdomains = find_subdomains(target_domain, "sublist3r/sublist3r.py")
        st.session_state.found_count = len(found_subdomains)
        if not found_subdomains:
            st.warning("No se descubrieron subdominios."); st.stop()

        with st.spinner(f"Fase 2/3: Validando {len(found_subdomains)} subdominios..."):
            active_subdomains = run_async_function(validate_subdomains_concurrently, found_subdomains)
        if not active_subdomains:
            st.warning("No se encontraron sitios activos."); st.stop()

        with st.spinner(f"Fase 3/3: Realizando escaneo profundo de tecnologías en {len(active_subdomains)} sitios..."):
            results_with_tech = run_async_function(run_full_tech_scan, active_subdomains)

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

    st.write("#### Tabla de Tecnologías Detectadas (Escaneo Profundo)")
    
    display_data = []
    for item in results:
        tech_list = item.get('technologies')
        if tech_list:
            tech_names = ", ".join(sorted([t['name'] for t in tech_list]))
            display_data.append({'Subdominio': item['subdomain'], 'URL': item['url'], 'Tecnologías': tech_names})
        else:
             display_data.append({'Subdominio': item['subdomain'], 'URL': item['url'], 'Tecnologías': 'N/A'})

    df_display = pd.DataFrame(display_data)
    
    # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
    # La advertencia era sobre un futuro cambio, esta sintaxis es la correcta por ahora.
    st.dataframe(df_display, use_container_width=True)