from funktion import fetch_pokemon_data
import pandas as pd

url = "https://api.pokemontcg.io/v2/cards"  # API URL
params = {"q": "types:Lightning AND (regulationMark:F OR regulationMark:G OR regulationMark:H)"}
lightning_cards = fetch_pokemon_data(url, params)

df = pd.DataFrame(lightning_cards)
print(df)