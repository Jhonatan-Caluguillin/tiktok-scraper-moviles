import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

# Carga las variables de entorno desde el archivo .env de forma segura
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ No se encontró la GEMINI_API_KEY. Asegúrate de crear tu archivo .env con la clave.")

def cargar_resultados(ruta_json="data/resultado_tiktok.json"):
    """Carga los datos reales extraídos por el scraper."""
    if not os.path.exists(ruta_json):
        print(f"Error: No se encontró {ruta_json}")
        return None
    with open(ruta_json, "r", encoding="utf-8") as f:
        return json.load(f)

def generar_analisis_bigfive_gemini(datos):
    """Envía las métricas y enlaces a Gemini usando la SDK oficial google-genai."""
    perfil = datos.get("perfil", {})
    videos = datos.get("videos", [])

    prompt = f"""
    Eres un psicólogo experto en análisis conductual y métricas de redes sociales.
    Analiza el perfil de TikTok del usuario '{perfil.get('username')}' con estas métricas:
    - Seguidores: {perfil.get('followers')}
    - Likes Totales: {perfil.get('total_likes')}
    - Videos procesados con sus enlaces y métricas:
    {json.dumps(videos, indent=2, ensure_ascii=False)}

    Por favor realiza:
    1. Una evaluación psicométrica del modelo Big Five (OCEAN) asignando puntajes de 0 a 100:
       - Openness (Apertura a la experiencia)
       - Conscientiousness (Responsabilidad / Tesón)
       - Extraversion (Extraversión)
       - Agreeableness (Amabilidad / Empatía)
       - Neuroticism (Inestabilidad emocional)
    2. Relaciona los LINKS DE LOS VIDEOS con el rasgo de personalidad que más respaldan.

    Devuelve ÚNICAMENTE un objeto JSON estricto con este formato exacto:
    {{
        "usuario": "{perfil.get('username')}",
        "fecha_analisis": "{datos.get('fecha_extraccion')}",
        "big_five_scores": {{
            "Openness": {{ "score": 85, "descripcion": "..." }},
            "Conscientiousness": {{ "score": 90, "descripcion": "..." }},
            "Extraversion": {{ "score": 75, "descripcion": "..." }},
            "Agreeableness": {{ "score": 80, "descripcion": "..." }},
            "Neuroticism": {{ "score": 20, "descripcion": "..." }}
        }},
        "asociacion_videos": [
            {{
                "url": "URL_DEL_VIDEO",
                "likes": "CANTIDAD_LIKES",
                "rasgo_relevante": "Rasgo OCEAN",
                "observacion": "Explicación de por qué respalda este rasgo"
            }}
        ],
        "conclusion_general": "Resumen psicométrico general del perfil."
    }}
    """

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Modelos vigentes recomendados por la API
    modelos_a_probar = ['gemini-3.8-flash', 'gemini-3.1-pro-preview']
    
    for modelo in modelos_a_probar:
        print(f"Enviando datos a la API de Gemini usando {modelo}...")
        for intento in range(3):
            try:
                response = client.models.generate_content(
                    model=modelo,
                    contents=prompt,
                    config=types.GenerateContentConfig(
                        response_mime_type="application/json"
                    )
                )
                return json.loads(response.text)
            except ServerError:
                print(f"⚠️ El modelo {modelo} está saturado. Reintentando en 3s... (Intento {intento + 1}/3)")
                time.sleep(3)
            except Exception as e:
                print(f"⚠️ Error inesperado con {modelo}: {e}")
                break

    raise Exception("No se pudo completar la solicitud con los modelos disponibles.")

def guardar_reporte(resultado, ruta_salida="data/analisis_bigfive.json"):
    """Guarda el informe en la carpeta data/."""
    os.makedirs(os.path.dirname(ruta_salida), exist_ok=True)
    with open(ruta_salida, "w", encoding="utf-8") as f:
        json.dump(resultado, f, ensure_ascii=False, indent=4)
    print(f"\n¡Análisis realizado exitosamente con Gemini y guardado en {ruta_salida}!")

if __name__ == "__main__":
    datos_tiktok = cargar_resultados()
    if datos_tiktok:
        analisis = generar_analisis_bigfive_gemini(datos_tiktok)
        guardar_reporte(analisis)