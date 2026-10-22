# TikTok Scraper & Analizador Psicométrico Big Five - Proyecto de Dispositivos Móviles

Este proyecto es un pipeline automatizado desarrollado en Python que combina scraping web con Playwright y el análisis inteligente de lenguaje natural mediante la API oficial de Google Gemini (`google-genai`). Su objetivo principal es extraer métricas de un perfil de TikTok y realizar una evaluación psicométrica de la personalidad del usuario basada en el modelo **Big Five (OCEAN)**.

---

## 📌 Características Principales

* **Métricas de Perfil:** Extracción de nombre de usuario, número de seguidores y total de likes acumulados.
* **Videos Recientes:** Identificación y recolección de las URLs de los últimos 10 videos publicados.
* **Métricas por Video:** Navegación interactiva sobre cada video para extraer la cantidad de likes, total de comentarios y textos de los comentarios.
* **Estrategia Anti-Bot:** Uso de indicadores `--disable-blink-features=AutomationControlled`, spoofing de User-Agent e interacción mediante clics reales para eludir restricciones de TikTok.
* **Análisis de IA (Big Five):** Procesamiento de métricas y videos mediante el modelo `gemini-3.8-flash` para evaluar los 5 rasgos de la personalidad (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism).
* **Asociación Conductual de Links:** Clasificación e interpretación psicométrica de cada URL individual de TikTok en función de su engagement y patrón de publicación.
* **Exportación Estructurada:** Guardado automático de los datos extraídos en `data/resultado_tiktok.json` y del informe psicológico final en `data/analisis_bigfive.json`.

---

## 📁 Estructura del Proyecto

```text
tiktok-scraper-moviles/
├── data/
│   ├── resultado_tiktok.json   # Archivo JSON generado con las métricas extraídas
│   └── analisis_bigfive.json   # Informe psicométrico generado por Gemini
├── scraper/
│   ├── __init__.py             # Inicializador del módulo scraper
│   ├── browser.py              # Configuración e inicialización del navegador con Playwright
│   ├── config.py               # URLs base, configuraciones globales y selectores CSS/data-e2e
│   └── parser.py               # Lógica principal de extracción del DOM y navegación interactiva
├── venv/                       # Entorno virtual de Python
├── .env                        # Variables de entorno (API Key de Gemini) - [Excluido de Git]
├── .gitignore                  # Archivos y carpetas excluidas del repositorio
├── analizador_bigfive.py       # Script de integración con la API de Gemini para evaluación OCEAN
├── main.py                     # Punto de entrada principal para ejecutar la extracción
├── README.md                   # Documentación detallada del proyecto
└── requirements.txt            # Lista de dependencias del proyecto

🛠️ Requisitos e Instalación

1. Clonar el repositorio y activar entorno virtual

git clone <https://github.com/Jhonatan-Caluguillin/tiktok-scraper-moviles>
cd tiktok-scraper-moviles
python -m venv venv
.\venv\Scripts\Activate.ps1

2. Instalar dependencias

pip install -r requirements.txt
playwright install chromium

3. Configurar clave de API
GEMINI_API_KEY=tu_api_key_aqui

🚀 Flujo de Ejecución

1. Extracción de datos de TikTok (Scraper)

python main.py

2. Análisis de Inteligencia Artificial (Big Five)

python analizador_bigfive.py

Datos obtenidos 

-Guarda los datos procesados en data/resultado_tiktok.json.
-Genera el informe psicométrico detallado en data/analisis_bigfive.json.