import requests
import pandas as pd

# Generelles
# Einstellungen für Pandas, sonst ist das Terminal zu klein
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

url = "https://api.pokemontcg.io/v2/cards"  # API URL
params = {"q": "set.legalities.standard:legal"}  # Query-Parameter um legale Pokemon zu kriegen, (in Dokumentation)
# params werden genutzt, um der API bei der Anfrage einen genaueren Parameter mitzugeben. Dadurch kann man filtern.
response = requests.get(url, params=params)



# Überprüft, ob die Anfrage erfolgreich war
if response.status_code == 200:
    data = response.json()  # JSON-Daten in lesbaren Python-Code umwandeln

    # 'data' enthält eine Struktur, die von der API vorgegeben ist
    cards = data.get("data", [])  # Holen der Karten (falls vorhanden)

    for card in cards:
        print(f'Name: {card["name"]}, Mark: {card["regulationMark"]}')
    df = pd.DataFrame(cards)    # Wandelt die gefetchten Daten in eine überschaubare Tabelle um
    print(df)

    # Hab versucht uns hier ne Excel-Datei zu erstellen, aber die wurde nicht richtig formatiert... :c
    # df.to_csv(r"C:/Sonstiges/Pokemon/legal-pokemon.csv", index=False, encoding="utf-8")
    # print("Die Datei wurde erfolgreich erstellt!")

else:
    print(f"Fehler: {response.status_code}")
