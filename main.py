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
