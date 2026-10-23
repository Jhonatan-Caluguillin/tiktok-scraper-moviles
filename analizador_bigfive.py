import json
import os
import time
from datetime import datetime
from dotenv import load_dotenv
from google import genai
from google.genai import types
from google.genai.errors import ServerError

# Intentamos cargar desde .env si existe, o usamos la API Key asignada directamente
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("⚠️ No se encontró la GEMINI_API_KEY.")

def cargar_resultados(ruta_json="data/resultado_tiktok.json"):
    """Carga los datos reales extraídos por el scraper."""
    if not os.path.exists(ruta_json):
        print(f"Error: No se encontró {ruta_json}")
        return None
    with open(ruta_json, "r", encoding="utf-8") as f:
        return json.load(f)

def generar_analisis_bigfive_gemini(datos):
    """Envía las métricas a Gemini para evaluar el Big Five sumando 100% por video y aplicando lógica de negocio."""
    perfil = datos.get("perfil", {})
    videos = datos.get("videos", [])

    prompt = f"""
    Eres un psicólogo experto en análisis conductual, métricas de redes sociales y estrategia de negocios digitales.
    Analiza el perfil de TikTok del usuario '{perfil.get('username')}' con las siguientes métricas:
    - Seguidores: {perfil.get('followers')}
    - Likes Totales: {perfil.get('total_likes')}
    - Videos procesados con sus enlaces y métricas:
    {json.dumps(videos, indent=2, ensure_ascii=False)}

    Por favor realiza lo siguiente:
    1. Una evaluación general psicométrica del modelo Big Five (OCEAN) para todo el perfil (puntajes de 0 a 100).
    2. Para CADA VIDEO del listado, asigna un porcentaje a cada uno de los 5 rasgos del Big Five (Openness, Conscientiousness, Extraversion, Agreeableness, Neuroticism) de tal manera que **la suma de los 5 rasgos de un mismo video dé exactamente el 100%** (ej. 20, 30, 20, 20, 10).
    3. Aplica una LÓGICA DE NEGOCIO COMERCIAL:
       - Calcula un "indice_comercial" (0 a 100) basado en el engagement relativo de likes/seguidores y el peso de los rasgos de personalidad proyectados.
       - Genera una "recomendacion_estrategica" clara para marcas (ej. "Ideal para campañas pagadas/Ads", "Contenido enfocado en fidelización comunitaria", "No recomendado para patrocinios").

    Devuelve ÚNICAMENTE un objeto JSON estricto con este formato exacto:
    {{
        "usuario": "{perfil.get('username')}",
        "fecha_analisis": "{datos.get('fecha_extraccion')}",
        "big_five_general": {{
            "Openness": {{ "score": 85, "descripcion": "Explicación general sobre apertura a la experiencia." }},
            "Conscientiousness": {{ "score": 90, "descripcion": "Explicación general sobre responsabilidad y orden." }},
            "Extraversion": {{ "score": 75, "descripcion": "Explicación general sobre extraversión e interacción." }},
            "Agreeableness": {{ "score": 80, "descripcion": "Explicación general sobre empatía y amabilidad." }},
            "Neuroticism": {{ "score": 20, "descripcion": "Explicación general sobre estabilidad emocional." }}
        }},
        "analisis_videos_detallado": [
            {{
                "url": "URL_DEL_VIDEO",
                "likes": "CANTIDAD_LIKES",
                "big_five_video": {{
                    "Openness": 25,
                    "Conscientiousness": 15,
                    "Extraversion": 40,
                    "Agreeableness": 10,
                    "Neuroticism": 10
                }},
                "logica_negocio": {{
                    "indice_comercial": 88.5,
                    "recomendacion_estrategica": "Excelente opción para pauta comercial debido a su alta extraversión y buen rendimiento."
                }}
            }}
        ],
        "conclusion_negocio": "Resumen ejecutivo combinando el perfil psicológico general con la viabilidad comercial del usuario para patrocinadores o marcas."
    }}
    """

    client = genai.Client(api_key=GEMINI_API_KEY)
    
    # Modelos vigentes
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

def guardar_reporte(resultado, ruta_salida="data/analisis_bigfive_negocio.json"):
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