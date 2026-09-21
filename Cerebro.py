import os

from dotenv import load_dotenv
load_dotenv()

import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Falta GEMINI_API_KEY en el archivo .env")

genai.configure(api_key=GEMINI_API_KEY)

MODELO_GEMINI = os.getenv("GEMINI_MODEL", "gemini-1.5-pro")
modelo = genai.GenerativeModel(MODELO_GEMINI)

def generar_respuesta(mensaje_usuario: str) -> str:
    prompt_sistema = """
    Eres un asistente virtual de la empresa.
    Responde a las dudas del usuario de forma amable y concisa.
    Mensaje del usuario: 
    """
    
    prompt_completo = prompt_sistema + mensaje_usuario.strip()
    
    try:
        respuesta = modelo.generate_content(prompt_completo)
        texto = getattr(respuesta, "text", None)
        if not texto:
            raise RuntimeError("Gemini devolvió una respuesta vacía")
        return texto.strip()
    except Exception as e:
        print(f"Error en el Cerebro (Gemini): {str(e)}")
        return "Lo siento, tuve un problema al procesar tu solicitud."