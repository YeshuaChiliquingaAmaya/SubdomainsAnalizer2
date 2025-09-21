# 🛡️ Plataforma de Ciberseguridad Unificada

Una herramienta de análisis de superficie de ataque que descubre, valida y evalúa subdominios y rutas sensibles a través de una interfaz de usuario web interactiva construida con Streamlit.

Este proyecto automatiza varias fases del reconocimiento inicial en una auditoría de seguridad, permitiendo al usuario obtener una visión general de la exposición digital de un dominio de forma rápida y sencilla.

*(Puedes reemplazar este enlace con una captura de pantalla de tu propia aplicación)*
-----

## ✨ Características Principales

  * **Descubrimiento de Subdominios:** Utiliza la potente herramienta `Sublist3r` para encontrar una lista exhaustiva de subdominios a partir de múltiples fuentes.
  * **Validación Concurrente:** Verifica de forma asíncrona y masiva qué subdominios están activos y responden a peticiones web, ahorrando tiempo y evitando errores.
  * **Fingerprinting de Tecnologías Profundo:** Combina dos métodos de escaneo para una identificación precisa:
      * Un escaneo rápido basado en `Wappalyzer`.
      * Un escaneo profundo y detallado con `WhatWeb`.
  * **Descubrimiento de Contenido Sensible:** Utiliza un diccionario personalizable para buscar directorios y archivos potencialmente expuestos (`/backup`, `.env`, `/admin`, etc.) en cada subdominio activo.
  * **Dashboard Interactivo:** Toda la funcionalidad está centralizada en una interfaz web amigable construida con `Streamlit`, mostrando los resultados en tablas y métricas claras.

-----

## 🛠️ Tecnologías Utilizadas

  * **Backend & Lógica:** Python 3.10+
  * **Interfaz de Usuario:** Streamlit
  * **Manejo de Datos:** Pandas
  * **Concurrencia:** Asyncio, Aiohttp
  * **Herramientas Externas:** Sublist3r, WhatWeb

-----

## 🚀 Guía de Instalación y Uso

Sigue estos pasos para configurar y ejecutar el proyecto en un sistema basado en Debian/Ubuntu.

### 1\. Prerrequisitos

Asegúrate de tener lo siguiente instalado en tu sistema:

  * Python 3.10 o superior
  * Git
  * `pip` (manejador de paquetes de Python)
  * Acceso `sudo` para instalar herramientas del sistema.

### 2\. Instalación

Abre tu terminal y sigue estos pasos uno por uno.

#### **Paso A: Clonar el Repositorio**

Clona este repositorio en tu máquina local.

```bash
git clone https://github.com/YeshuaChiliquingaAmaya/SubdomainsAnalizer2.git
cd SubdomainsAnalizer2
```

#### **Paso B: Instalar Herramientas Externas**

La plataforma depende de `whatweb` para el escaneo profundo. Instálalo a través de `apt`.

```bash
sudo apt-get update
sudo apt-get install whatweb -y
```

#### **Paso C: Configurar el Entorno Virtual de Python**

Es una buena práctica aislar las dependencias del proyecto.

```bash
# Crear el entorno virtual
python3 -m venv venv

# Activar el entorno virtual
source venv/bin/activate
```

*(Verás `(venv)` al principio de tu línea de comandos, indicando que está activo).*

#### **Paso D: Instalar Dependencias del Proyecto**

Este proyecto utiliza varias librerías de Python, incluyendo `Sublist3r`.

```bash
# 1. Instalar las librerías principales desde requirements.txt
pip install -r requirements.txt

# 2. Clonar Sublist3r dentro de la carpeta del proyecto
git clone https://github.com/aboul3la/Sublist3r.git sublist3r

# 3. Instalar las dependencias específicas de Sublist3r
pip install -r sublist3r/requirements.txt
```

#### **Paso E: Crear el Diccionario de Rutas**

La herramienta necesita una lista de palabras para buscar rutas sensibles.

```bash
# Crea el archivo wordlist.txt
touch wordlist.txt
```

Ahora, **abre el archivo `wordlist.txt`** y pega el siguiente contenido:

```
.env
.env.local
.env.backup
config.php.bak
backup
backup.zip
backup.tar.gz
database.sql
admin
administrator
login
dashboard
admin-panel
uploads
wp-admin
wp-login.php
.git
.svn
logs
log.txt
error.log
```

### 3\. Ejecución

¡Ya está todo listo\! Para iniciar la interfaz web, ejecuta el siguiente comando desde la carpeta raíz del proyecto:

```bash
streamlit run dashboard.py
```

Se abrirá automáticamente una pestaña en tu navegador web. Simplemente ingresa el dominio que deseas analizar (ej. `example.com`) y haz clic en **"Iniciar Análisis Profundo"**.

-----

## 🗺️ Hoja de Ruta (Futuras Mejoras)

Este proyecto tiene un gran potencial para crecer. Algunas de las funcionalidades planeadas para el futuro incluyen:

  * **Integración con la NVD:** Conectar las tecnologías encontradas con vulnerabilidades (CVEs) en tiempo real.
  * **Análisis de Riesgo Avanzado:** Implementar el módulo de puntuación de riesgo utilizando los datos reales de CVEs.
  * **Escaneo DAST:** Integrar herramientas como OWASP ZAP para un escaneo de vulnerabilidades activo.
  * **Reportes Mejorados:** Expandir el reporte en PDF para incluir todos los hallazgos (tecnologías, rutas, etc.).
  * **Persistencia de Datos:** Guardar los resultados de los escaneos en una base de datos.