import random

POKEMON_KARTEN = ["charmander", "growlithe", "squirtle", "psyduck"]
class SpielerZustand:
    def __init__(self, deck, name="Spieler"):
        self.name = name
        self.deck = deck
        self.hand = []
        self.aktives_pokemon = None
        self.bank = []
        self.preis_karten = ["preis"] * 6  # 6 Preiskarten
        self.ablagestapel = []
        self.supporter_gespielt = False
        self.stadium = None
        self.diese_runde_energie_angelegt = False

    def ziehe_starthand(self):
        random.shuffle(self.deck)
        while len(self.hand) < 7:
            if not any(ist_pokemon(card) for card in self.deck):
                print(f"[{self.name}] mischt das Deck neu, weil kein Pokémon vorhanden ist!")
                random.shuffle(self.deck)
            self.hand.append(self.deck.pop(0))

    def ziehe_karte(self):
        if self.deck:
            gezogene_karte = self.deck.pop(0)
            self.hand.append(gezogene_karte)
            print(f"[{self.name}] zieht Karte: {gezogene_karte}")
        else:
            print(f"[{self.name}] hat keine Karten mehr im Deck!")

    def status(self):
        print(f"\n[{self.name}] Status:")
        print(f"- Aktives Pokémon: {self.aktives_pokemon}")
        print(f"- Handkarten: {self.hand}")
        print(f"- Bank: {[p['name'] for p in self.bank]}")
        print(f"- Preiskarten: {len(self.preis_karten)}")
        print(f"- Verbleibende Deckkarten: {len(self.deck)}")
        print()

# Hilfsfunktionen für Kartenarten
def ist_energy(card):
    return "energy" in card.lower()

def ist_pokemon(card):
    return card.lower() in POKEMON_KARTEN

def ist_trainer(card):
    return "trainer" in card.lower()

# Energie anlegen
def spielt_energiekarte(player, pokemon, energie_karte):
    if player.diese_runde_energie_angelegt:
        print(f"[{player.name}] hat bereits eine Energiekarte angelegt!")
        return False

    if ist_energy(energie_karte):
        pokemon['energy'].append(energie_karte)
        player.hand.remove(energie_karte)
        player.diese_runde_energie_angelegt = True
        print(f"[{player.name}] legt {energie_karte} an {pokemon['name']}.")
        return True
    else:
        print(f"[{player.name}] {energie_karte} ist keine gültige Energiekarte!")
        return False

# Angreifen
def angreifen(player, gegner):
    if player.aktives_pokemon and gegner.aktives_pokemon:
        print(f"[{player.name}] greift mit {player.aktives_pokemon['name']} an!")
        gegner.aktives_pokemon['hp'] -= player.aktives_pokemon['damage']
        print(f"[{gegner.name}] {gegner.aktives_pokemon['name']} verliert {player.aktives_pokemon['damage']} HP.")
        if gegner.aktives_pokemon['hp'] <= 0:
            print(f"[{gegner.name}] {gegner.aktives_pokemon['name']} wurde besiegt!")
            if player.preis_karten:
                player.preis_karten.pop()
                print(f"[{player.name}] nimmt eine Preiskarte. Verbleibend: {len(player.preis_karten)}")
            gegner.aktives_pokemon = None
            aktiviere_bank_pokemon(gegner)

# Bank aktivieren
def aktiviere_bank_pokemon(player):
    if player.bank:
        player.aktives_pokemon = player.bank.pop(0)
        print(f"[{player.name}] aktiviert {player.aktives_pokemon['name']} von der Bank.")
    else:
        print(f"[{player.name}] hat keine Pokémon mehr auf der Bank!")

# Spielzug
def spielzug(player, gegner):
    print(f"\n[{player.name}] ist am Zug.")
    player.ziehe_karte()
    player.diese_runde_energie_angelegt = False

    # Pokémon ausspielen
    for card in player.hand[:]:
        if ist_pokemon(card):
            if player.aktives_pokemon is None:
                player.aktives_pokemon = {"name": card, "hp": 50, "damage": 30, "energy": []}
                player.hand.remove(card)
                print(f"[{player.name}] setzt {player.aktives_pokemon['name']} als aktives Pokémon.")
            elif len(player.bank) < 5:
                player.bank.append({"name": card, "hp": 50, "damage": 30, "energy": []})
                player.hand.remove(card)
                print(f"[{player.name}] legt {card} auf die Bank.")

    # Energie anlegen
    for card in player.hand[:]:
        if ist_energy(card) and player.aktives_pokemon:
            if spielt_energiekarte(player, player.aktives_pokemon, card):
                break

    # Angreifen + Spielinformation anzeigen
    angreifen(player, gegner)
    player.status()


# Spielende prüfen
def game_over(player, gegner):
    return (
            not player.deck or not gegner.deck or
            len(player.preis_karten) == 0 or len(gegner.preis_karten) == 0
    )

def bestimme_sieger(player, gegner):
    if len(player.preis_karten) == 0:
        return f"{player.name} gewinnt (Keine Preiskarten mehr vorhanden)!"
    elif len(gegner.preis_karten) == 0:
        return f"{gegner.name} gewinnt (Keine Preiskarten mehr vorhanden)!"
    elif not player.deck:
        return f"{gegner.name} gewinnt (Deckende)!"
    elif not gegner.deck:
        return f"{player.name} gewinnt (Deckende)!"
    return "Unentschieden!"

# Simulation starten
def simuliere_spiel(player_deck, gegner_deck):
    player = SpielerZustand(player_deck, "Player")
    gegner = SpielerZustand(gegner_deck, "Gegner")

    player.ziehe_starthand()
    gegner.ziehe_starthand()

    runde = 1
    while not game_over(player, gegner):
        print(f"\n==== Runde {runde} ====")
        spielzug(player, gegner)
        if game_over(player, gegner):
            break
        spielzug(gegner, player)
        runde += 1

    return bestimme_sieger(player, gegner)

# Beispiel-Decks
player_deck = ["fire_energy", "charmander", "fire_energy", "growlithe", "trainer_supporter"] * 4
gegner_deck = ["water_energy", "squirtle", "water_energy", "psyduck", "trainer_item"] * 4

ergebnis = simuliere_spiel(player_deck, gegner_deck)
print(f"\nSpielende: {ergebnis}")
