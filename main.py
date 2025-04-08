
from flask import Flask, request
from threading import Thread
import time

app = Flask(__name__)

@app.route('/')
def home():
    return "Bot Floki activo 🛡️🔥"

def run():
    app.run(host='0.0.0.0', port=10000)

def keep_alive():
    t = Thread(target=run)
    t.start()

def iniciar_bot():
    print("🔥 FlokiBot iniciando...")
    while True:
        print("⚔️ Floki está buscando apuestas con mejor porcentaje...")
        time.sleep(60)

if __name__ == "__main__":
    keep_alive()
    iniciar_bot()
