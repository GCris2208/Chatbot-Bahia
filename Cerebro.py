import os
from google import genai

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
if not GEMINI_API_KEY:
    raise RuntimeError("Falta GEMINI_API_KEY")

# Inicialización del nuevo SDK oficial
cliente = genai.Client(api_key=GEMINI_API_KEY)

def generar_respuesta(mensaje_usuario: str) -> str:
    prompt_sistema = (
        "Eres el asistente virtual de la empresa Bahía. "
        "Responde a las dudas del usuario de forma amable, concisa y muy útil.\n\n"
        "Mensaje del usuario: "
    )
    
    try:
        # La nueva sintaxis de ejecución para el modelo 2.5 Flash
        respuesta = cliente.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt_sistema + mensaje_usuario.strip()
        )
        return respuesta.text.strip()
    except Exception as e:
        print(f"Error en el Cerebro (Gemini): {str(e)}")
        return "Lo siento, tuve un problema al procesar tu solicitud."