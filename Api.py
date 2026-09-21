import logging
from fastapi import BackgroundTasks, FastAPI, Request, Response
from dotenv import load_dotenv

load_dotenv()

from Chat import enviar_mensaje
from Cerebro import generar_respuesta

app = FastAPI()
logger = logging.getLogger(__name__)

@app.get("/")
def raiz():
    return {"mensaje": "Servidor del Chatbot Bahia activo (Modo Telegram)."}

def procesar_mensaje(chat_id: int, texto_usuario: str) -> None:
    logger.info("Procesando mensaje del chat %s", chat_id)
    
    respuesta_ia = generar_respuesta(texto_usuario)
    enviar_mensaje(chat_id, respuesta_ia)

@app.post("/webhook")
async def telegram_webhook(request: Request, background_tasks: BackgroundTasks):
    try:
        # Telegram envía un JSON estructurado, no un formulario URL-encoded
        data = await request.json()
    except Exception:
        return Response(content="Formato inválido", status_code=400)

    # Extraer el ID del chat y el texto del mensaje de la estructura de Telegram
    if "message" in data and "text" in data["message"]:
        chat_id = data["message"]["chat"]["id"]
        texto_usuario = data["message"]["text"]
        
        # Enviar el procesamiento a segundo plano para no hacer esperar a Telegram
        background_tasks.add_task(procesar_mensaje, chat_id, texto_usuario)

    # Confirmar recepción (Status 200) para que Telegram no reintente el envío
    return Response(status_code=200)