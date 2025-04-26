# Aufgabe: Erstellen Sie eine PPM-Datei mit einem Farbverlauf.
def save_ppm(filename, width, height):
    with open(filename, 'w') as f:
        # PPM-Header
        f.write(f"P3\n{width} {height}\n255\n")
        
        # Farbverlauf generieren
        for y in range(height):
            for x in range(width):
                r = int(255 * (x / width))  # Rotanteil
                g = int(255 * (y / height))  # Grünanteil
                b = 0  # Blauanteil
                f.write(f"{r} {g} {b} ")
            f.write("\n")

# Beispielaufruf
import os
print(os.getcwd())
save_ppm("gradient.ppm", 256, 256)