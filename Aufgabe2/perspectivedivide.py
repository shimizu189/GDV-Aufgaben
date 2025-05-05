# Definition des Würfels (näher an die Kamera schieben)
cube = [
    [-1.0, -1.0, -4],
    [-1.0, 1.0, -4],
    [-1.0, -1.0, -5],
    [-1.0, 1.0, -5],
    [1.0, -1.0, -4],
    [1.0, 1.0, -4],
    [1.0, -1.0, -5],
    [1.0, 1.0, -5],
]

# Bildgröße
width = 800
height = 800

# Mittelpunkt des Bildes
cx = width // 2
cy = height // 2

# Sichtfeld (Field of View)
fov = 1.0  # Skalierungsfaktor für die Projektion

# Funktion zur Perspektivprojektion
def perspective_divide(vertex):
    x, y, z = vertex
    if z == 0:
        raise ValueError("Z-Koordinate darf nicht 0 sein (Division durch 0).")
    x_proj = fov * x / -z
    y_proj = fov * y / -z
    return x_proj, y_proj

# Funktion zur Konvertierung von 2D-Koordinaten in Pixelkoordinaten
def to_pixel_coordinates(x, y):
    pixel_x = int(cx + x * width / 2)
    pixel_y = int(cy - y * height / 2)  # Y-Achse ist invertiert
    return pixel_x, pixel_y

# Liste der projizierten Pixelkoordinaten
projected_points = []

for vertex in cube:
    x_proj, y_proj = perspective_divide(vertex)
    pixel_x, pixel_y = to_pixel_coordinates(x_proj, y_proj)
    projected_points.append((pixel_x, pixel_y))

# Erstellen eines leeren Bildes (Hintergrundfarbe ändern, z.B. zu Schwarz)
image = [[(0, 0, 0) for _ in range(width)] for _ in range(height)]

# Zeichnen der Punkte des Würfels (z.B. rot)
for x, y in projected_points:
    if 0 <= x < width and 0 <= y < height:  # Punkt muss im Bildbereich liegen
        image[y][x] = (255, 0, 0)  # Rot

# Schreiben der .ppm-Datei
with open("cube.ppm", "w") as f:
    # Header der PPM-Datei
    f.write("P3\n")
    f.write(f"{width} {height}\n")
    f.write("255\n")
    # Pixel-Daten
    for row in image:
        for pixel in row:
            f.write(f"{pixel[0]} {pixel[1]} {pixel[2]} ")
        f.write("\n")

print("Die Datei 'cube.ppm' wurde erfolgreich erstellt.")