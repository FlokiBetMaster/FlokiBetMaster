# scraper.py
import requests
from bs4 import BeautifulSoup

def obtener_partidos():
    try:
        url = "https://www.goal.com/en/live-scores"
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")

        # 🧪 Aquí aún va scraping real si lo necesitas
        return [
            {
                "equipo1": "Team A",
                "equipo2": "Team B",
                "hora": "12:00",
                "liga": "Premier League",
                "equipos": "Team A vs Team B"
            },
            {
                "equipo1": "Team C",
                "equipo2": "Team D",
                "hora": "14:00",
                "liga": "LaLiga",
                "equipos": "Team C vs Team D"
            }
        ]
    except Exception as e:
        print("❌ Error en scraper:", e)
        return []
