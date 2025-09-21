# Plataforma de Ciberseguridad Unificada 🛡️

Una herramienta de código abierto para el reconocimiento y análisis de la superficie de ataque digital. Esta plataforma automatiza el descubrimiento, validación y análisis de subdominios para identificar posibles vectores de riesgo.

## ✨ Características Principales

-   **Descubrimiento de Subdominios:** Utiliza la potente herramienta [Sublist3r](https://github.com/aboul3la/Sublist3r) para encontrar una lista exhaustiva de subdominios.
-   **Validación Concurrente:** Verifica de forma asíncrona y ultra-rápida qué subdominios están activos y responden a peticiones web.
-   **Detección Profunda de Tecnologías:** Identifica el stack tecnológico de cada sitio activo, combinando la rapidez de [Wappalyzer](https://www.wappalyzer.com/) con la profundidad de [WhatWeb](https://github.com/urbanadventurer/WhatWeb).
-   **Descubrimiento de Contenido Sensible:** Busca directorios y archivos potencialmente expuestos (como `/backup`, `.env`, `/admin`) utilizando un diccionario personalizable.
-   **Interfaz de Usuario Web:** Todo el poder de la herramienta está gestionado a través de una interfaz interactiva y fácil de usar creada con [Streamlit](https://streamlit.io/).

## 📸 Vistazo a la Aplicación


*(Aquí puedes añadir una captura de pantalla de tu dashboard en funcionamiento)*

---

## ⚙️ Prerrequisitos

Antes de empezar, asegúrate de tener instalado lo siguiente en tu sistema (preferiblemente basado en Debian/Ubuntu):

-   **Python 3.10** o superior
-   **Git** para clonar los repositorios
-   **WhatWeb** (herramienta de escaneo profundo)

Puedes instalar WhatWeb con el siguiente comando:
```bash
sudo apt-get update && sudo apt-get install whatweb -y
```

---

## 🚀 Instalación y Puesta en Marcha

Sigue estos pasos para tener la plataforma funcionando en tu máquina local.

### 1. Clona este Repositorio

Abre tu terminal y clona el código fuente de la plataforma.
```bash
git clone [URL-DE-TU-REPOSITORIO-AQUÍ]
cd [NOMBRE-DE-LA-CARPETA-DEL-PROYECTO]
```

### 2. Crea y Activa un Entorno Virtual

Es una buena práctica aislar las dependencias del proyecto para evitar conflictos.
```bash
# Crear el entorno
python3 -m venv venv

# Activar el entorno (lo harás cada vez que trabajes en el proyecto)
source venv/bin/activate
```
Verás `(venv)` al principio del prompt de tu terminal, lo que indica que el entorno está activo.

### 3. Descarga Sublist3r

La plataforma utiliza Sublist3r como motor de descubrimiento. Clónalo dentro de la carpeta del proyecto.
```bash
git clone [https://github.com/aboul3la/Sublist3r.git](https://github.com/aboul3la/Sublist3r.git) sublist3r
```

### 4. Instala todas las Dependencias de Python

Este comando instalará todas las librerías que necesita tanto la plataforma principal como Sublist3r.
```bash
pip install -r requirements.txt
pip install -r sublist3r/requirements.txt
```
*(Nota: Asegúrate de que tu archivo `requirements.txt` esté actualizado con todas las librerías que hemos usado: `streamlit`, `pandas`, `nest_asyncio`, `aiohttp`, `requests`, `python-whois`, etc.)*

---

## ▶️ Cómo Usar la Aplicación

Una vez que la instalación esté completa, lanzar la interfaz es muy sencillo.

1.  **Asegúrate de que tu entorno virtual (`venv`) esté activado.**
2.  **Ejecuta el siguiente comando** en la carpeta raíz del proyecto:

    ```bash
    streamlit run dashboard.py
    ```

3.  **Abre tu navegador web** y ve a la URL local que te indica la terminal (normalmente `http://localhost:8501`).
4.  **Ingresa el dominio** que deseas analizar en el campo de texto y haz clic en el botón **"Iniciar Análisis Completo"**.
5.  **¡Observa la magia!** La plataforma te mostrará el progreso en tiempo real y presentará los resultados en tablas interactivas al finalizar.

---

## 📂 Estructura del Proyecto

```
.
├── sublist3r/            # Repositorio de la herramienta Sublist3r
├── modules/              # Módulos principales de nuestra lógica
│   ├── content_discovery.py
│   ├── deep_scanner.py
│   ├── discovery.py
│   ├── ml_classifier.py
│   ├── orchestrator.py
│   ├── report.py
│   ├── subdomain_finder.py
│   ├── tech_detector.py
│   └── validate.py
├── dashboard.py          # El código de la interfaz de usuario (Streamlit)
├── main.py               # Script principal para ejecución en consola (opcional)
├── requirements.txt      # Dependencias de Python
├── template.html         # Plantilla para el reporte en PDF
└── wordlist.txt          # Diccionario para el descubrimiento de contenido
```