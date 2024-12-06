import requests
import pandas as pd
from funktion import fetch_pokemon_data
from panda_einstellungen import terminal

url = "https://api.pokemontcg.io/v2/cards"  # API URL
params = {"q": "regulationMark:F OR regulationMark:G OR regulationMark:H"}
fetch_pokemon_data(url, params)




# Hab versucht uns hier ne Excel-Datei zu erstellen, aber die wurde nicht richtig formatiert... :c
# df.to_csv(r"C:/Sonstiges/Pokemon/legal-pokemon.csv", index=False, encoding="utf-8")
# print("Die Datei wurde erfolgreich erstellt!")