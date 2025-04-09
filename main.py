# main.py

from flask import Flask
import threading
import time
from your_bot_module import start_bot  # Asegúrate de importar tu lógica aquí

# Crea el servidor Flask mínimo para mantener el servicio vivo
app = Flask(__name__)

@app.route('/')
def home():
    return "FlokiBetMaster is running and scraping Copa Libertadores + Sudamericana!"

# Ejecuta el bot en un hilo paralelo
def run_bot():
    print("[🧠 FlokiBot] Iniciando scraping y análisis de partidos...")
    start_bot()  # Aquí va tu lógica principal

# Inicia el hilo del bot
threading.Thread(target=run_bot).start()

# Ejecuta Flask para que Render detecte el puerto
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=10000)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
