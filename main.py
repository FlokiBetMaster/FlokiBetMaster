import requests
import time
import selenium.webdriver as webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from telegram import Bot

# Configuración de Telegram
TELEGRAM_BOT_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
TELEGRAM_CHAT_ID = "2130752167"
bot = Bot(token=TELEGRAM_BOT_TOKEN)

# Función para obtener cuotas de Bwin
def obtener_cuotas_bwin():
    url = "https://api.bwin.com/api/sportsbook"  # Ejemplo, debes usar la API correcta o web scraping
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

# Función para calcular apuestas de valor
def calcular_apuestas_de_valor(cuotas_bwin):
    apuestas_valor = []
    for evento in cuotas_bwin['eventos']:
        for apuesta in evento['mercados']:
            cuota = float(apuesta['cuota'])
            probabilidad_justa = 1 / cuota  # Cálculo simple, puedes mejorar con modelos avanzados
            if cuota > (1 / (probabilidad_justa * 0.9)):  # 10% de margen
                apuestas_valor.append({
                    'evento': evento['nombre'],
                    'apuesta': apuesta['nombre'],
                    'cuota': cuota
                })
    return apuestas_valor

# Función para enviar apuestas a Telegram
def enviar_apuestas_telegram(apuestas):
    if apuestas:
        mensaje = "📢 Apuestas de valor encontradas:\n"
        for ap in apuestas:
            mensaje += f"🏆 {ap['evento']} - {ap['apuesta']} - Cuota: {ap['cuota']}\n"
        bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=mensaje)
    else:
        print("No hay apuestas de valor.")

# Función para apostar automáticamente en Bwin
def apostar_en_bwin(apuestas):
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://www.bwin.com/")
    time.sleep(5)
    
    # Inicio de sesión (debes modificarlo con tus credenciales y estructura de la web)
    driver.find_element(By.ID, "login-username").send_keys("TU_USUARIO")
    driver.find_element(By.ID, "login-password").send_keys("TU_PASSWORD")
    driver.find_element(By.ID, "login-submit").click()
    time.sleep(5)
    
    # Colocar apuestas
    for ap in apuestas:
        driver.get("https://www.bwin.com/es/sports")  # Navega al evento
        time.sleep(3)
        
        # Lógica para encontrar y apostar en el mercado correcto
        # (Depende de la estructura de la web, debes inspeccionar los elementos)
        
        driver.find_element(By.XPATH, "//boton_de_apuesta").click()
        time.sleep(2)
        driver.find_element(By.XPATH, "//input_monto").send_keys("1000")  # Ejemplo de apuesta de 10,000 COP
        driver.find_element(By.XPATH, "//boton_confirmar").click()
        time.sleep(3)
    
    driver.quit()

# Flujo principal
def ejecutar_bot():
    cuotas_bwin = obtener_cuotas_bwin()
    if cuotas_bwin:
        apuestas_valor = calcular_apuestas_de_valor(cuotas_bwin)
        enviar_apuestas_telegram(apuestas_valor)
        apostar_en_bwin(apuestas_valor)
    else:
        print("No se pudo obtener cuotas de Bwin.")

# Ejecutar cada cierto tiempo
while True:
    ejecutar_bot()
    time.sleep(3600)  # Ejecuta cada hora


