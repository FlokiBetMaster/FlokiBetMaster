# predict.py

def generar_prediccion(partido):
    if not partido:
        print("⚠️ Advertencia: partido vacío.")
        return None

    texto = partido.get("equipos", "").lower()
    if not texto:
        equipo1 = partido.get("equipo1", "")
        equipo2 = partido.get("equipo2", "")
        texto = f"{equipo1} vs {equipo2}".lower()

    # 🧠 Aquí puedes agregar lógica de predicción básica
    return {
        "partido": texto.title(),
        "prediccion": "Over 2.5",
        "confianza": "74%",
        "stake": "3.5%",
        "url_apostar": "https://www.bwin.com/"
    }
