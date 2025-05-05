# Aufgabe: Erstellen Sie eine PPM-Datei mit einem Farbverlauf.
import os

def save_ppm(filename, width, height, frame):
    with open(filename, 'w') as f:
        # PPM-Header
        f.write(f"P3\n{width} {height}\n255\n")
        
        # Farbverlauf generieren
        for y in range(height):
            for x in range(width):
                r = (x + frame) % 256  # Rotanteil mit Zeitkomponente
                g = (y + frame) % 256  # Grünanteil mit Zeitkomponente
                b = 0  # Blauanteil bleibt konstant
                f.write(f"{r} {g} {b} ")
            f.write("\n")

# Sequenz von PPM-Dateien erstellen
output_dir = "frames"
os.makedirs(output_dir, exist_ok=True)

width, height = 256, 256
start_frame, end_frame = 0, 20  # Anzahl der Frames

for frame in range(start_frame, end_frame):
    filename = os.path.join(output_dir, f"frame_{frame}.ppm")
    print(f"Erstelle Frame: {filename}")
    save_ppm(filename, width, height, frame)