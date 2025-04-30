from flask import Flask, jsonify
from scraper import obtener_partidos

app = Flask(__name__)

@app.route('/api/partidos')
def api_partidos():
    partidos = obtener_partidos()
    return jsonify(partidos)

if __name__ == '__main__':
    app.run(port=5000)
