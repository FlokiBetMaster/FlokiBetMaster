import telegram
from telegram.ext import Updater, CommandHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
import requests
import json
import schedule
import time
import threading
import logging

# Configuración
TELEGRAM_TOKEN = "7673667307:AAHxupSKq1xC-QP2Pl6q_wQEXSJMzwuefCU"
TELEGRAM_CHAT_ID = "2130752167"
bot = telegram.Bot(token=TELEGRAM_TOKEN)
BANK_FILE = "bank.json"
logging.basicConfig(filename="flokibot.log", level=logging.INFO)

# Gestión de bank
def load_bank():
    try:
        with open(BANK_FILE, "r") as f:
            return json.load(f)
    except:
        return {"balance": 100000, "bets": []}

def save_bank(bank):
    with open(BANK_FILE, "w") as f:
        json.dump(bank, f)

# Calcular stake (de stake.py, adaptado)
def calcular_stake(confianza, bank_balance):
    confianza = float(confianza.replace("%", "") if isinstance(confianza, str) else confianza * 100)
    if confianza >= 85:
        return bank_balance * 0.05
    elif confianza >= 70:
        return bank_balance * 0.03
    else:
        return bank_balance * 0.01

# URL dinámica para Bwin
def get_bwin_url(match):
    teams = match.lower().replace(" vs ", "-vs-")
    return f"https://www.bwin.com/es/sports/futbol-4/partido/{teams}"

# Enviar predicciones
def send_predictions_to_telegram():
    logging.info("Enviando predicciones a Telegram...")
    try:
        bank = load_bank()
        response = requests.get("http://localhost:5000/predictions")
        predictions = response.json()
        sent_matches = set()
        for pred in predictions:
            if pred["match"] not in sent_matches and len(sent_matches) < 3:
                sent_matches.add(pred["match"])
                stake = calcular_stake(pred["confidence"], bank["balance"])
                message = (f"🏆 {pred['match']}\n"
                           f"Apuesta: {pred['bet']}\n"
                           f"Cuota: {pred['odds']}\n"
                           f"Stake: {stake:.2f} COP\n"
                           f"Confianza: {pred['confidence']*100:.1f}%")
                keyboard = [[InlineKeyboardButton("Apostar en Bwin", url=get_bwin_url(pred["match"]))]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, reply_markup=reply_markup)
                bank["bets"].append({
                    "match": pred["match"],
                    "bet": pred["bet"],
                    "stake": stake,
                    "odds": pred["odds"],
                    "date": time.strftime("%Y-%m-%d %H:%M:%S")
                })
                save_bank(bank)
        logging.info("Predicciones enviadas con éxito")
    except Exception as e:
        logging.error(f"Error: {e}")

# Comandos
def stats(update, context):
    bank = load_bank()
    message = (f"💰 Bank: {bank['balance']:.2f} COP\n"
               f"📊 Apuestas realizadas: {len(bank['bets'])}")
    update.message.reply_text(message)

def bets(update, context):
    bank = load_bank()
    if not bank["bets"]:
        update.message.reply_text("No hay apuestas registradas.")
        return
    message = "📜 Historial de apuestas:\n"
    for bet in bank["bets"][-5:]:
        message += f"{bet['date']} - {bet['match']} ({bet['bet']}): {bet['stake']:.2f} COP @ {bet['odds']}\n"
    update.message.reply_text(message)

def performance(update, context):
    bank = load_bank()
    initial_bank = 100000
    roi = ((bank["balance"] - initial_bank) / initial_bank) * 100
    update.message.reply_text(f"📈 ROI: {roi:.2f}%")

# Programar envío
schedule.every(6).hours.do(send_predictions_to_telegram)

def run_scheduler():
    while True:
        schedule.run_pending()
        time.sleep(60)

def main():
    updater = Updater(TELEGRAM_TOKEN, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(CommandHandler("stats", stats))
    dp.add_handler(CommandHandler("bets", bets))
    dp.add_handler(CommandHandler("performance", performance))
    updater.start_polling()
    threading.Thread(target=run_scheduler, daemon=True).start()

if __name__ == "__main__":
    main()

def calcular_stake_kelly(bank, odds, prob):
    b = odds - 1
    p = prob / 100
    q = 1 - p
    kelly_fraction = (b * p - q) / b
    return max(0, min(bank * kelly_fraction * 0.5, bank * 0.03))  # Mitad de Kelly, máximo 3%

# Modificar send_predictions_to_telegram
def send_predictions_to_telegram():
    logging.info("Enviando predicciones a Telegram...")
    try:
        bank = load_bank()
        response = requests.get("http://localhost:5000/predictions")
        predictions = response.json()
        sent_matches = set()
        for pred in predictions:
            if pred["match"] not in sent_matches and len(sent_matches) < 3:
                sent_matches.add(pred["match"])
                stake = calcular_stake_kelly(bank["balance"], pred["odds"], pred["confidence"] * 100)
                message = (f"🏆 {pred['match']}\n"
                           f"Apuesta: {pred['bet']}\n"
                           f"Cuota: {pred['odds']}\n"
                           f"Stake: {stake:.2f} COP\n"
                           f"Confianza: {pred['confidence']*100:.1f}%")
                keyboard = [[InlineKeyboardButton("Apostar en Bwin", url=get_bwin_url(pred["match"]))]]
                reply_markup = InlineKeyboardMarkup(keyboard)
                bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message, reply_markup=reply_markup)
                bank["bets"].append({
                    "match": pred["match"],
                    "bet": pred["bet"],
                    "stake": stake,
                    "odds": pred["odds"],
                    "date": time.strftime("%Y-%m-%d %H:%M:%S"),
                    "result": "pending"
                })
                save_bank(bank)
        logging.info("Predicciones enviadas con éxito")
    except Exception as e:
        logging.error(f"Error: {e}")

# Comando para registrar resultados
def result(update, context):
    bank = load_bank()
    if not bank["bets"]:
        update.message.reply_text("No hay apuestas para actualizar.")
        return
    try:
        args = context.args
        if len(args) != 2:
            update.message.reply_text("Uso: /result <índice> <win/lose>")
            return
        index = int(args[0]) - 1
        outcome = args[1].lower()
        if index < 0 or index >= len(bank["bets"]):
            update.message.reply_text("Índice inválido.")
            return
        bet = bank["bets"][index]
        if outcome == "win":
            bank["balance"] += bet["stake"] * (bet["odds"] - 1)
            bet["result"] = "win"
        elif outcome == "lose":
            bank["balance"] -= bet["stake"]
            bet["result"] = "lose"
        else:
            update.message.reply_text("Resultado debe ser 'win' o 'lose'.")
            return
        save_bank(bank)
        update.message.reply_text(f"Apuesta {index + 1} actualizada: {bet['match']} ({bet['result']}). Bank: {bank['balance']:.2f} COP")
    except Exception as e:
        update.message.reply_text(f"Error: {e}")

# Agregar al dispatcher
dp.add_handler(CommandHandler("result", result))