import os
import google.generativeai as genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Falta GEMINI_API_KEY")

genai.configure(api_key=GEMINI_API_KEY)

# Usamos Flash: máxima velocidad para evitar timeouts en Telegram
modelo = genai.GenerativeModel("gemini-1.5-flash")

def generar_respuesta(mensaje_usuario: str) -> str:
    prompt_sistema = (
        "Eres el asistente virtual de la empresa Bahía. "
        "Responde a las dudas del usuario de forma amable, concisa y muy útil.\n\n"
        "Mensaje del usuario: "
    )
    
    try:
        respuesta = modelo.generate_content(prompt_sistema + mensaje_usuario.strip())
        return respuesta.text.strip()
    except Exception as e:
        print(f"Error en el Cerebro (Gemini): {str(e)}")
        return "Lo siento, tuve un problema al procesar tu solicitud."