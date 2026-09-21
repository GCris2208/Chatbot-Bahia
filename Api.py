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
    return {"mensaje": "Servidor del Chatbot Bahia activo (Modo Twilio)."}

def procesar_mensaje(numero_remitente: str, texto_usuario: str) -> None:
    logger.info("Mensaje recibido de %s", numero_remitente)
    
    respuesta_ia = generar_respuesta(texto_usuario)
    
    if not enviar_mensaje(numero_remitente, respuesta_ia):
        logger.error("No se pudo enviar la respuesta a %s", numero_remitente)

@app.post("/webhook")
async def procesar_mensajes(
    request: Request,
    background_tasks: BackgroundTasks,
):
    try:
        # Twilio envia los datos en formato URL-encoded form
        form_data = await request.form()
    except Exception:
        return Response(content="Formato invalido", status_code=400)

    numero_remitente = form_data.get("From")
    texto_usuario = form_data.get("Body")

    if not numero_remitente or not texto_usuario:
        return Response(content="Datos insuficientes", status_code=400)

    # Enviar el procesamiento a segundo plano para no bloquear a Twilio
    background_tasks.add_task(procesar_mensaje, numero_remitente, texto_usuario)

    # Twilio requiere una respuesta XML (TwiML) valida
    return Response(content="<Response></Response>", media_type="application/xml", status_code=200)