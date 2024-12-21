import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder


# Funktion, um die CSV-Datei zu laden und die Daten für den Apriori-Algorithmus vorzubereiten
def prepare_data_for_apriori(file_path):
    # Lade das Deck aus der CSV-Datei
    df = pd.read_csv(file_path)
    df_pokemon = df[df['Type'] == 'Pokemon']
    # Die Karten aus der "Card Name"-Spalte extrahieren und pro Deck in Listen umwandeln
    # transactions = df.groupby('Deck Name')['Card Name'].apply(list).tolist()
    transactions = df_pokemon.groupby('Deck Name')['Card Name'].apply(list).tolist()

    # Umwandeln der Transaktionen in das für Apriori erforderliche Format
    te = TransactionEncoder()
    te_ary = te.fit(transactions).transform(transactions)
    df_transformed = pd.DataFrame(te_ary, columns=te.columns_)

    return df_transformed


# Funktion, um Assoziationsregeln aus den Deck-Daten zu erstellen
def generate_association_rules(file_path, min_support, min_threshold):
    # Daten für den Apriori-Algorithmus vorbereiten
    print(f"Starten der Datenvorbereitung...")
    df_transformed = prepare_data_for_apriori(file_path)

    # Häufige Itemsets extrahieren
    print(f"Starten des Apriori-Algorithmus mit min_support={min_support}")
    frequent_itemsets = apriori(df_transformed, min_support=min_support, use_colnames=True)
    print(f"Frequente Itemsets gefunden: {len(frequent_itemsets)}")


    if frequent_itemsets.empty:
        print("Keine häufigen Itemsets gefunden.")
        return None


    print(f"Generierung der Assoziationsregeln...")
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_threshold, num_itemsets=None)
    print(f"Anzahl der generierten Regeln: {len(rules)}")

    # Wenn keine Regeln gefunden wurden, gebe eine Meldung aus
    if rules.empty:
        print("Keine Assoziationsregeln gefunden.")
        return None

    return rules


# Beispielaufruf: Assoziationsregeln für das Deck erstellen
output_file = "decks.csv"  # Der Pfad zur CSV-Datei, die die Decks enthält
rules = generate_association_rules(output_file, min_support=0.4, min_threshold=1)

# Ausgabe der generierten Assoziationsregeln
if rules is not None:
    print("Generierte Assoziationsregeln:")
    print(rules)

    # Speicherung der Assoziationsregeln in einer csv.-Datei
    rules.to_csv("assoziationsregeln-low.csv", index=False)
else:
    print("Es wurden keine Assoziationsregeln generiert.")
