# -*- coding: utf-8 -*-

import time
from scraper import obtener_partidos
from predict import generar_prediccion
from stake import calcular_stake

print("=================================")
print(">> Ejecutando FlokiBot...")
print("=================================")
print("FlokiBot en modo apuestas 24/7...\n")

while True:
    try:
        partidos = obtener_partidos()

        if not partidos:
            print("⚠️ No hay partidos activos.")
            time.sleep(10)
            continue

        for partido in partidos:
            prediccion = generar_prediccion(partido)
            if not prediccion:
                continue

            stake = calcular_stake(prediccion["confianza"])

            print(f"""
=========================================
Partido: {prediccion['partido']}
Predicción sugerida: {prediccion['prediccion']}
Confianza estimada: {prediccion['confianza']}
Stake recomendado: {stake}%
Enlace para apostar: {prediccion['url_apostar']}
=========================================
""")

        time.sleep(60)  # Pausa de 60 segundos

    except Exception as e:
        print(f"Se produjo un error: {e}")
        time.sleep(10)  # Pausa corta en caso de error

    finally:
        # Este bloque puede ser usado si necesitas ejecutar algo independientemente de si ocurrió un error
        print("Ciclo completado. Reintentando en breve...")
