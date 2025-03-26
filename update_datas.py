import os
import json

# Configurazioni
base_url = "https://example.com"  # Sostituisci con il tuo dominio
img_folder = "static/img"
data_file = "static/data/datas.json"

# Ottieni la lista dei file di immagini nella cartella static/img
image_files = [f for f in os.listdir(img_folder) if f.endswith('.png')]

# Crea la lista dei percorsi in formato URL
# image_urls = [f"{base_url}/{img_folder}/{file}" for file in image_files]
image_urls = [f"{img_folder}/{file}" for file in image_files]

# Carica il file JSON esistente (se presente)
if os.path.exists(data_file):
    with open(data_file, 'r') as f:
        data = json.load(f)
else:
    data = {}

# Aggiorna la lista delle immagini
data['images'] = image_urls

# Scrivi il JSON aggiornato nel file
with open(data_file, 'w') as f:
    json.dump(data, f, indent=4)

print(f"File {data_file} aggiornato con successo!")