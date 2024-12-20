
player_deck_rate = 0

# Füttern durch Gewinne / Verluste, Winrate (Anzahl wins / Anzahl losses + 1 / - 1)
def fitness_evaluation(ergebnis):
    if ergebnis == "Player gewinnt!":
        player_deck_rate += 0.5
    else:
        player_deck_rate -= 0.5


fitness_evaluation(ergebnis)