from playwright.sync_api import sync_playwright

def iniciar_navegador():
    """Inicializa Playwright simulando un navegador real para evitar el bloqueo de TikTok."""
    p = sync_playwright().start()
    
    # Agregamos flags para desactivar la detección de automatización
    browser = p.chromium.launch(
        headless=False,
        args=[
            "--disable-blink-features=AutomationControlled",
            "--start-maximized"
        ]
    )
    
    context = browser.new_context(
        viewport={"width": 1280, "height": 800},
        user_agent="Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
        locale="es-ES",
        timezone_id="America/Guayaquil"
    )
    
    page = context.new_page()
    
    # Inyectamos script para ocultar navigator.webdriver
    page.add_init_script("""
        Object.defineProperty(navigator, 'webdriver', {
            get: () => undefined
        });
    """)
    
    return p, browser, page