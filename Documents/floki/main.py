
from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def home():
    return "Bot Floki activo 🛡️🔥"

@app.route("/prediccion")
def prediccion():
    # Simulación de una predicción de apuesta
    return jsonify({
        "partido": "Flamengo vs Palmeiras",
        "apuesta": "Más de 2.5 goles",
        "probabilidad": "82%",
        "stake": 2
    })

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=10000)
