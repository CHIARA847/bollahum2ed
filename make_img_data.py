from PIL import Image, ImageDraw, ImageFont
import os

# Funzione per generare un'immagine placeholder
def generate_placeholder(width, height, filename):
    # Crea un'immagine con sfondo grigio
    image = Image.new('RGB', (width, height), color='#cccccc')
    draw = ImageDraw.Draw(image)

    # Aggiunge il testo con le dimensioni
    text = f"{width}x{height}"
    font = ImageFont.load_default()  # Usa il font di default

    # Calcola le dimensioni del testo
    bbox = draw.textbbox((0, 0), text, font=font)
    text_width = bbox[2] - bbox[0]
    text_height = bbox[3] - bbox[1]

    # Posiziona il testo al centro dell'immagine
    draw.text(
        ((width - text_width) / 2, (height - text_height) / 2),  # Posizione del testo
        text,
        fill='black',
        font=font
    )

    # Salva l'immagine
    image.save(filename)

# Crea la cartella static/img se non esiste
if not os.path.exists('static/img'):
    os.makedirs('static/img')

# Genera 10 immagini con dimensioni diverse
for i in range(1, 11):
    width = 100 * i
    height = 100 * i
    filename = f"static/img/placeholder_{width}x{height}.png"
    generate_placeholder(width, height, filename)
    print(f"Generata: {filename}")

print("Tutte le immagini sono state generate con successo!")