from funktion import fetch_pokemon_data
import pandas as pd

url = "https://api.pokemontcg.io/v2/cards"  # API URL
params = {"q": "types:Fire AND (regulationMark:F OR regulationMark:G OR regulationMark:H)"}
fire_cards = fetch_pokemon_data(url, params)

df = pd.DataFrame(fire_cards)
print(df)