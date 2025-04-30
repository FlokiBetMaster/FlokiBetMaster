import requests

API_KEY = "a6fdcc949cb6e52a9f9fbbfff6e44b30"

def obtener_cuota(partido):
    try:
        url = "https://api.the-odds-api.com/v4/sports/soccer/odds/"
        params = {
            "apiKey": API_KEY,
            "regions": "eu",
            "markets": "totals"
        }
        res = requests.get(url, params=params)
        if res.status_code == 200:
            data = res.json()
            if data and "bookmakers" in data[0]:
                return data[0]["bookmakers"][0]["markets"][0]["outcomes"][0]["price"]
    except:
        pass
    return 1.90
