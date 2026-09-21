import os
import requests
from dotenv import load_dotenv

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

def enviar_mensaje(chat_id: int, texto_respuesta: str) -> bool:
    if not TELEGRAM_BOT_TOKEN:
        print("Error: Falta TELEGRAM_BOT_TOKEN")
        return False

    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    
    payload = {
        "chat_id": chat_id,
        "text": texto_respuesta,
    }

    try:
        respuesta = requests.post(url, json=payload, timeout=15)
        if respuesta.status_code == 200:
            return True
        return False
    except requests.RequestException:
        return False