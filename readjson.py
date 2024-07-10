import json

# Nome del file JSON da aprire
nome_file = "channel_messages.json"

# Apre il file in modalità lettura
with open(nome_file, "r") as file:
    # Carica il contenuto del file JSON in un dizionario
    dati = json.load(file)

# Stampa il contenuto del dizionario
for m in dati:
    print("ALERT:",m["message"])
    print("DATA:",m["date"])
    print("DESCRIPTION:",m["media"]["webpage"].get("description","N/A"))
