import requests
import pandas as pd
from panda_einstellungen import terminal

terminal()      # Zugriff auf panda_einstellungen


# Ruft die Pokémon-Daten von der API ab; returns List: Eine Liste von Pokémon-Daten, falls erfolgreich. Sonst None.
def fetch_pokemon_data(api_url, params):
    all_cards = []  # Hier sollen alle ausgegebenen Karten gespeichert werden
    page = 1        # Beginn der ersten Seite

    while True:
        print(f"Fetching page {page}...")
        params["page"] = page
        response = requests.get(api_url, params=params)

        if response.status_code == 200:     # Überprüft, ob die Anfrage erfolgreich war
            data = response.json()  # JSON-Daten in lesbaren Python-Code umwandeln

            cards = data.get("data", [])  # Holen der Karten (falls vorhanden)

            if not cards:
                break

            all_cards.extend(cards)
            page += 1
        else:
            print(f"Fehler: {response.status_code}")

    return all_cards