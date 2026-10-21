import time
from scraper.config import SELECTORS, TIKTOK_URL

def obtener_datos_perfil(page, url_perfil=TIKTOK_URL):
    """Navega al perfil de TikTok y permite superar bloqueos visuales manualmente."""
    print(f"Navegando a: {url_perfil}")
    page.goto(url_perfil, wait_until="domcontentloaded")
    
    print("\n" + "="*60)
    print("[ATENCIÓN] Si TikTok requiere verificación:")
    print("1. Resuelve el captcha o haz clic en 'Actualizar'.")
    print("2. Verifica que las miniaturas de los videos se vean en pantalla.")
    print("="*60)
    input("Presiona ENTER en esta terminal una vez que los videos estén visibles...")

    username = page.inner_text(SELECTORS["profile_username"]) if page.query_selector(SELECTORS["profile_username"]) else "N/A"
    followers = page.inner_text(SELECTORS["profile_followers"]) if page.query_selector(SELECTORS["profile_followers"]) else "N/A"
    likes = page.inner_text(SELECTORS["profile_likes"]) if page.query_selector(SELECTORS["profile_likes"]) else "N/A"

    return {
        "username": username,
        "followers": followers,
        "total_likes": likes
    }

def obtener_ultimos_10_videos(page):
    """Retorna los enlaces de los últimos 10 videos encontrados."""
    page.evaluate("window.scrollBy(0, 300)")
    time.sleep(2)

    videos_links = []
    anchors = page.query_selector_all('a[href*="/video/"]')
    for a in anchors:
        href = a.get_attribute("href")
        if href and href not in videos_links:
            videos_links.append(href)
            if len(videos_links) >= 10:
                break

    return videos_links[:10]

def extraer_detalle_video(page, url_video):
    """Abre el video haciendo clic en la tarjeta del perfil y extrae sus métricas reales."""
    print(f"Scrapeando video vía clic interactivo...")
    
    video_id = url_video.split("/")[-1] if "/" in url_video else url_video
    selector_video = f'a[href*="{video_id}"]'

    try:
        elem = page.query_selector(selector_video)
        if elem:
            elem.scroll_into_view_if_needed()
            time.sleep(1)
            elem.click(force=True)
            time.sleep(3)  # Tiempo para que cargue la interfaz del reproductor

        # Intentar extraer likes
        likes_elem = page.query_selector(SELECTORS["video_likes"])
        likes = likes_elem.inner_text().strip() if likes_elem else "0"

        # Intentar extraer cantidad de comentarios
        comments_elem = page.query_selector(SELECTORS["video_comments_count"])
        comments_count = comments_elem.inner_text().strip() if comments_elem else "0"

        # Extraer comentarios
        comentarios = []
        elementos_comentario = page.query_selector_all(SELECTORS["comment_item"])
        for elem_com in elementos_comentario[:5]:
            texto = elem_com.inner_text().strip().replace("\n", " ")
            if texto:
                comentarios.append(texto)

        # Si no hay comentarios por restricción de TikTok, agregar mensaje explicativo
        if not comentarios:
            comentarios = ["Sin comentarios públicos o requieren iniciar sesión"]

        # Cerramos la vista de video
        page.keyboard.press("Escape")
        time.sleep(1.5)

        return {
            "url": url_video,
            "likes": likes,
            "comments_count": comments_count,
            "comentarios": comentarios
        }
    except Exception as e:
        print(f"Aviso al procesar mediante clic: {e}")
        return {
            "url": url_video,
            "likes": "0",
            "comments_count": "0",
            "comentarios": []
        }