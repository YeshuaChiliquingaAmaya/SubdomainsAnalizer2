# dashboard.py (versión final corregida)

import streamlit as st
import pandas as pd
import asyncio
import nest_asyncio

nest_asyncio.apply()

from modules.subdomain_finder import find_subdomains
from modules.validate import validate_subdomains_concurrently
# ¡CAMBIO! Importamos ambas funciones del orquestador
from modules.orchestrator import run_full_tech_scan, run_content_discovery_scan

st.set_page_config(page_title="Plataforma de Ciberseguridad", page_icon="🛡️", layout="wide")

def run_async_function(func, *args):
    return asyncio.run(func(*args))

# Inicializamos el estado de la sesión
if 'scan_results' not in st.session_state: st.session_state.scan_results = None
if 'domain_scanned' not in st.session_state: st.session_state.domain_scanned = ""
if 'found_count' not in st.session_state: st.session_state.found_count = 0
if 'sensitive_paths_results' not in st.session_state: st.session_state.sensitive_paths_results = None

st.title("🛡️ Plataforma de Ciberseguridad Unificada")
target_domain = st.text_input("Ingresa un dominio para analizar", placeholder="tes.edu.ec")

if st.button("Iniciar Análisis Completo"):
    if target_domain:
        st.session_state.scan_results = None
        st.session_state.sensitive_paths_results = None

        with st.spinner("Fase 1/4: Descubriendo subdominios..."):
            found_subdomains = find_subdomains(target_domain, "sublist3r/sublist3r.py")
        st.session_state.found_count = len(found_subdomains)
        if not found_subdomains: st.warning("No se descubrieron subdominios."); st.stop()

        with st.spinner(f"Fase 2/4: Validando {len(found_subdomains)} subdominios..."):
            active_subdomains = run_async_function(validate_subdomains_concurrently, found_subdomains)
        if not active_subdomains: st.warning("No se encontraron sitios activos."); st.stop()

        with st.spinner(f"Fase 3/4: Realizando escaneo de tecnologías en {len(active_subdomains)} sitios..."):
            results_with_tech = run_async_function(run_full_tech_scan, active_subdomains)
        st.session_state.scan_results = results_with_tech
        st.session_state.domain_scanned = target_domain
        
        # --- ¡AQUÍ ESTÁ LA CORRECCIÓN! ---
        # Reemplazamos el bucle 'for' con una única llamada a nuestro nuevo orquestador.
        with st.spinner(f"Fase 4/4: Buscando rutas sensibles en {len(active_subdomains)} sitios..."):
            all_sensitive_paths = run_async_function(run_content_discovery_scan, active_subdomains)
        st.session_state.sensitive_paths_results = all_sensitive_paths
        
        st.success("¡Análisis Completo finalizado!")
        st.rerun()
    else:
        st.error("Por favor, ingresa un dominio para analizar.")

# --- SECCIÓN DE VISUALIZACIÓN DE RESULTADOS (sin cambios) ---
if st.session_state.scan_results is not None:
    results = st.session_state.scan_results
    domain = st.session_state.domain_scanned
    found_count = st.session_state.found_count
    sensitive_paths = st.session_state.sensitive_paths_results

    st.subheader(f"Resultados para: {domain}")
    col1, col2 = st.columns(2)
    col1.metric("Subdominios Descubiertos", found_count)
    col2.metric("Sitios Activos Analizados", len(results))
    st.divider()

    tab1, tab2 = st.tabs(["🔎 Tecnologías Detectadas", "🔥 Rutas Sensibles Encontradas"])

    with tab1:
        st.write("#### Tabla de Tecnologías Detectadas (Escaneo Profundo)")
        display_data = []
        for item in results:
            tech_names = ", ".join(sorted([t['name'] for t in item.get('technologies', [])])) or 'N/A'
            display_data.append({'Subdominio': item['subdomain'], 'URL': item['url'], 'Tecnologías': tech_names})
        df_display = pd.DataFrame(display_data)
        st.dataframe(df_display, use_container_width=True)

    with tab2:
        st.write("#### Lista de Posibles Rutas, Directorios y Archivos Sensibles")
        if not sensitive_paths:
            st.info("No se encontraron rutas sensibles con el diccionario actual.")
        else:
            for subdomain, paths_found in sensitive_paths.items():
                with st.expander(f"Subdominio: {subdomain} ({len(paths_found)} encontrados)"):
                    df_paths = pd.DataFrame(paths_found)
                    # --- ¡CORRECCIÓN DE LA ADVERTENCIA! ---
                    st.dataframe(df_paths, use_container_width=True)