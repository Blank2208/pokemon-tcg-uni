import pandas as pd
from mlxtend.frequent_patterns import apriori, association_rules
from mlxtend.preprocessing import TransactionEncoder

# Funktion, um die CSV-Datei zu laden und die Daten für den Apriori-Algorithmus vorzubereiten
def prepare_data_for_apriori(file_path):
    # Gesamte Deckliste(n) werden geladen -> Alle Meta Decks in diesem Jahr (2024)
    df = pd.read_csv(file_path)

    # Filterungen
    # df_pokemon = df[df['Type'] == 'Pokemon']
    # df_trainer = df[df['Type'] == 'Trainer']

    transactions_list = []

    for deck_name, group in df.groupby('Deck Name'):
        transaction = []
        for _, row in group.iterrows():
            transaction.extend([row['Card Name']])
        transactions_list.append(transaction)

    # Umwandeln der Transaktionen in Apriori Format
    te = TransactionEncoder()
    te_ary = te.fit(transactions_list).transform(transactions_list)
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

    # Generierung der Assoziationsregeln
    print(f"Generierung der Assoziationsregeln...")
    rules = association_rules(frequent_itemsets, metric="lift", min_threshold=min_threshold, num_itemsets= None)
    print(f"Anzahl der generierten Regeln: {len(rules)}")

    # Wenn keine Regeln gefunden wurden, gebe eine Meldung aus
    if rules.empty:
        print("Keine Assoziationsregeln gefunden.")
        return None

    return rules


# Assoziationsaufruf
output_file = "decklisten/decks_anpassung.csv"  # Decks, ohne die Spalte "Quantity", sondern untereinander geschrieben
rules = generate_association_rules(output_file, min_support=0.15, min_threshold=1)

# Ausgabe der generierten Assoziationsregeln
if rules is not None:
    print("Generierte Assoziationsregeln:")
    print(rules)

    # Speicherung der Assoziationsregeln in einer csv.-Datei
    rules.to_csv("assoziationsregeln-015.csv", index=False)
else:
    print("Es wurden keine Assoziationsregeln generiert.")

