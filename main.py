import requests
import time

# --- CONFIGURACIÓN TELEGRAM ---
TOKEN = '7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU'
CHAT_ID = '2130752167'
API_URL = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

# --- MENSAJE DE TESTEO ---
def enviar_mensaje(mensaje):
    try:
        payload = {
            'chat_id': CHAT_ID,
            'text': mensaje
        }
        response = requests.post(API_URL, data=payload)
        if response.status_code != 200:
            print('Error al enviar mensaje:', response.text)
    except Exception as e:
        print('Error:', str(e))

# --- LOOP PRINCIPAL ---
def run_bot():
    enviar_mensaje("⚡ FlokiBot está en línea, listo para vikingear ⚔️")
    while True:
        # Aquí irán las predicciones y el stake automático más adelante
        enviar_mensaje("Ejemplo de alerta automática 🧠 Probabilidad: 87% - Stake: 2.5%")
        time.sleep(3600)  # Envía 1 vez por hora (modificable)

if __name__ == '__main__':
    run_bot()
import threading
import time
import flask

# Inicia el bot en un hilo separado
def run_bot():
    # Aquí va tu lógica principal (scraping, análisis, Telegram)
    start_bot()  # o como se llame tu función principal

bot_thread = threading.Thread(target=run_bot)
bot_thread.start()

# Crea un servidor Flask mínimo para que Render detecte un puerto
app = flask.Flask(__name__)

@app.route('/')
def home():
    return "FlokiBetMaster is running."

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
