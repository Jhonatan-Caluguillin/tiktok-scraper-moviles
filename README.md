# TikTok Scraper - Proyecto de Dispositivos Móviles

Este proyecto es un scraper automatizado desarrollado en **Python** utilizando **Playwright**. Su objetivo principal es realizar la extracción de datos de un perfil de TikTok sin depender de APIs oficiales o extensiones de navegador de terceros.

---

## 📌 Características Principales

- **Métricas de Perfil**: Extracción de nombre de usuario, número de seguidores y total de likes acumulados.
- **Videos Recientes**: Identificación y recolección de las URLs de los últimos 10 videos publicados.
- **Métricas por Video**: Navegación interactiva sobre cada video para extraer la cantidad de likes, total de comentarios y textos de los comentarios.
- **Exportación Estructurada**: Guardado automático de los datos extraídos en formato **JSON** dentro de `data/resultado_tiktok.json`.
- **Estrategia Anti-Bot**: Uso de indicadores `--disable-blink-features=AutomationControlled`, spoofing de User-Agent e interacción mediante clics reales para evitar bloqueos por parte de TikTok.

---

## 📁 Estructura del Proyecto

```text
tiktok-scraper-moviles/
├── data/
│   └── resultado_tiktok.json   # Archivo JSON generado con las métricas extraídas
├── scraper/
│   ├── __init__.py             # Inicializador del módulo scraper
│   ├── browser.py              # Configuración e inicialización del navegador con Playwright
│   ├── config.py               # URLs base, configuraciones globales y selectores CSS/data-e2e
│   └── parser.py               # Lógica principal de extracción del DOM y navegación interactiva
├── venv/                       # Entorno virtual de Python
├── .gitignore                  # Archivos y carpetas excluidas del repositorio
├── main.py                     # Punto de entrada principal para ejecutar la extracción
├── README.md                   # Documentación detallada del proyecto
└── requirements.txt            # Lista de dependencias del proyecto