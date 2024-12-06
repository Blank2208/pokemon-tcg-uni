import requests
import pandas as pd

# Generelles
# Einstellungen für Pandas, sonst ist das Terminal zu klein
pd.set_option('display.max_rows', 3794)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1500)

url = "https://api.pokemontcg.io/v2/cards"  # API URL
params = {"q": "regulationMark:F OR regulationMark:G OR regulationMark:H"}
# Query-Parameter um legale Pokemon zu kriegen, (in Dokumentation)
# params werden genutzt, um der API bei der Anfrage einen genaueren Parameter mitzugeben. Dadurch kann man filtern.
response = requests.get(url, params=params)

all_cards = []  # Hier sollen alle ausgegebenen Karten gespeichert werden
page = 1        # Beginn der ersten Seite

# Überprüft, ob die Anfrage erfolgreich war
while True:
    print(f"Fetching page {page}...")
    params["page"] = page
    response = requests.get(url, params=params)

    if response.status_code == 200:
        data = response.json()  # JSON-Daten in lesbaren Python-Code umwandeln

        # 'data' enthält eine Struktur, die von der API vorgegeben ist
        cards = data.get("data", [])  # Holen der Karten (falls vorhanden)

        if not cards:
            break

        all_cards.extend(cards)
        page += 1

    else:
        print(f"Fehler: {response.status_code}")

df = pd.DataFrame(all_cards)    # Wandelt die gefetchten Daten in eine überschaubare Tabelle um
print(df)

# Hab versucht uns hier ne Excel-Datei zu erstellen, aber die wurde nicht richtig formatiert... :c
# df.to_csv(r"C:/Sonstiges/Pokemon/legal-pokemon.csv", index=False, encoding="utf-8")
# print("Die Datei wurde erfolgreich erstellt!")