import os
import random
import requests
from bs4 import BeautifulSoup
from urllib.parse import urljoin
import shutil

# Configurazioni
baseurl = "https://www.arteantidoto.com"  # Sostituisci con la tua URL di base
temp_dir = "temp_images"
output_dir = "static/img"

# Crea le cartelle se non esistono
os.makedirs(temp_dir, exist_ok=True)
os.makedirs(output_dir, exist_ok=True)

# Funzione per scaricare un'immagine
def download_image(url, folder, image_name):
    # Crea il nome del file nel formato {image_name}_{id}.png
    filename = f"{image_name}.png"
    local_path = os.path.join(folder, filename)

    # Scarica l'immagine
    with requests.get(url, stream=True) as r:
        if r.status_code == 200:
            with open(local_path, 'wb') as f:
                shutil.copyfileobj(r.raw, f)
            print(f"Scaricata: {filename}")
        else:
            print(f"Errore durante il download di {url}")
    return local_path

# Funzione principale
def main():
    # Fase 1: Leggi gli href dei tag <a> che contengono un <img>
    response = requests.get(f"{baseurl}/artisti")
    soup = BeautifulSoup(response.text, 'html.parser')
    links = []
    for a_tag in soup.find_all('a', href=True):
        if a_tag.find('img'):
            links.append(a_tag['href'])

    # Contatore globale per l'ID delle immagini
    image_id = 0

    # Fase 2: Scarica tutte le immagini di tutti i link
    for link in links:
        full_url = urljoin(baseurl, link)
        response = requests.get(full_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        opere_link = None

        # Cerca il tag <a> che contiene un <p> con testo "Opere"
        for a_tag in soup.find_all('a', href=True):
            p_tag = a_tag.find('p')
            if p_tag and p_tag.get_text(strip=True) == "Opere":
                opere_link = a_tag['href']
                break

        if opere_link:
            if not opere_link.startswith('http'):
                opere_link = urljoin(baseurl, opere_link)

            # Estrai il nome della pagina "opere" (es. /artisti/artista/opereartista -> opereartista)
            opere_name = opere_link.strip('/').split('/')[-1]

            # Scarica tutte le immagini nella pagina delle opere
            response = requests.get(opere_link)
            soup = BeautifulSoup(response.text, 'html.parser')
            images = soup.find_all('img')
            for img in images:
                img_url = urljoin(opere_link, img['src'])
                # Usa il nome della pagina "opere" e l'ID per il nome del file
                download_image(img_url, temp_dir, f"{opere_name}_{image_id}")
                image_id += 1

    # Fase 3: Seleziona 10 immagini a caso e copiale nella cartella static/img
    all_images = [os.path.join(temp_dir, f) for f in os.listdir(temp_dir)]  # Lista di tutte le immagini
    selected_images = random.sample(all_images, min(10, len(all_images)))  # Seleziona 10 immagini casuali
    for img_path in selected_images:
        shutil.copy(img_path, output_dir)  # Copia le immagini in static/img

    # Pulisci la cartella temporanea
    shutil.rmtree(temp_dir)
    os.makedirs(temp_dir, exist_ok=True)

if __name__ == "__main__":
    main()