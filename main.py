import json
import os
from datetime import datetime
from scraper.browser import iniciar_navegador
from scraper.parser import (
    obtener_datos_perfil,
    obtener_ultimos_10_videos,
    extraer_detalle_video
)
from scraper.config import TIKTOK_URL

def main():
    print("=== INICIANDO SCRAPER DE TIKTOK ===")
    
    # 1. Iniciar el navegador
    p, browser, page = iniciar_navegador()
    
    try:
        # 2. Extraer datos generales del perfil
        perfil_info = obtener_datos_perfil(page, TIKTOK_URL)
        print(f"\n[Perfil Encontrado] Usuario: {perfil_info['username']} | Seguidores: {perfil_info['followers']} | Likes: {perfil_info['total_likes']}")
        
        # 3. Obtener los enlaces de los últimos 10 videos
        print("\nBuscando los últimos 10 videos...")
        links_videos = obtener_ultimos_10_videos(page)
        print(f"Se encontraron {len(links_videos)} videos.")
        
        # 4. Extraer detalles de cada video (likes, comentarios, etc.)
        videos_detalles = []
        for index, link in enumerate(links_videos, start=1):
            print(f"\nProcesando video {index} de {len(links_videos)}...")
            detalle = extraer_detalle_video(page, link)
            videos_detalles.append(detalle)
            
        # 5. Consolidar la estructura de datos final
        resultado_final = {
            "fecha_extraccion": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "perfil": perfil_info,
            "videos": videos_detalles
        }
        
        # 6. Guardar en un archivo JSON en la carpeta data/
        os.makedirs("data", exist_ok=True)
        nombre_archivo = "data/resultado_tiktok.json"
        with open(nombre_archivo, "w", encoding="utf-8") as f:
            json.dump(resultado_final, f, ensure_ascii=False, indent=4)
            
        print(f"\n¡Scraping completado con éxito! Datos guardados en {nombre_archivo}")

    except Exception as e:
        print(f"\n[ERROR CRÍTICO DURANTE EL SCRAPING]: {e}")
        
    finally:
        # Cerrar navegador de forma segura
        browser.close()
        p.stop()
        print("Navegador cerrado.")

if __name__ == "__main__":
    main()