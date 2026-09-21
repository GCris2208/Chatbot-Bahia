import requests

# 1. Coloca aquí el token exacto que te dio BotFather
TOKEN = "8687915189:AAEdkoi8o4g6y1CUaBOWlazbRsgJKkH5UcQ"

# 2. Coloca aquí la URL pública que te dio Render al finalizar el Paso 5
URL_RENDER = "https://chatbot-bahia.onrender.com"

# Armamos la ruta exacta
url_telegram = f"https://api.telegram.org/bot{TOKEN}/setWebhook?url={URL_RENDER}/webhook"

print("Estableciendo conexión con Telegram...")
try:
    respuesta = requests.get(url_telegram)
    print("Resultado:")
    print(respuesta.text)
except Exception as e:
    print("Hubo un error:", e)