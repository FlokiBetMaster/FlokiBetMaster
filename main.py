from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
import time
import requests
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID

# Configurar opciones de Chrome
options = Options()
options.add_argument('--headless')
options.add_argument('--disable-gpu')
options.add_argument('--no-sandbox')
options.add_argument('--disable-dev-shm-usage')

service = Service(executable_path='C:/Users/57310/Desktop/chrome_drive/chromedriver.exe')
driver = webdriver.Chrome(service=service, options=options)

try:
    # Ir al sitio web
    driver.get("https://www.flashscore.com/")

    # Esperar un poco para que cargue
    time.sleep(5)

    # Obtener el contenido principal (puedes personalizar esto)
    contenido = driver.find_element(By.TAG_NAME, "body").text

    # Enviar a Telegram
    mensaje = f"✅ Scraping completado:\n\n{contenido[:3500]}"  # límite de caracteres
    url = f"https://api.telegram.org/bot{TELEGRAM_BOT_TOKEN}/sendMessage"
    data = {"chat_id": TELEGRAM_CHAT_ID, "text": mensaje}
    requests.post(url, data=data)

    print("✅ Scraping finalizado y mensaje enviado a Telegram.")
except Exception as e:
    print(f"❌ Error: {e}")
finally:
    driver.quit()

