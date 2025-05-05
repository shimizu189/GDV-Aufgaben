import math
import os

def save_ppm(width, height, buffer, time):
    filename = f"frame_{time:03d}.ppm"
    with open(filename, "w") as f:
        f.write(f"P3\n{width} {height}\n255\n")
        for i in range(0, len(buffer), 3):
            f.write(f"{buffer[i]} {buffer[i+1]} {buffer[i+2]} ")
            if (i // 3 + 1) % width == 0:
                f.write("\n")

def set_raster_coordinate(x, y, r, g, b):
    if 0 <= x < width and 0 <= y < height:
        index = (y * width + x) * 3
        buffer[index] = r
        buffer[index + 1] = g
        buffer[index + 2] = b

def perspective_divide(p, screen_distance):
    return [p[0] / -p[2], p[1] / -p[2], p[2]]

def view_to_raster(v, width, height):
    x = int((v[0] + 1) * 0.5 * width)
    y = int((1 - (v[1] + 1) * 0.5) * height)
    return [x, y]

def m4_x_m4(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(4)) for j in range(4)] for i in range(4)]

def vec3_to_vec4(v):
    return [v[0], v[1], v[2], 1.0]

def mult_vec3_m4(v, m):
    v4 = vec3_to_vec4(v)
    return [sum(v4[j] * m[j][i] for j in range(4)) for i in range(4)]

def rot_x(degrees):
    radians = math.radians(degrees)
    return [
        [1, 0, 0],
        [0, math.cos(radians), -math.sin(radians)],
        [0, math.sin(radians), math.cos(radians)]
    ]

def m3_to_m4(m):
    return [
        [m[0][0], m[0][1], m[0][2], 0],
        [m[1][0], m[1][1], m[1][2], 0],
        [m[2][0], m[2][1], m[2][2], 0],
        [0, 0, 0, 1]
    ]

# Bildgröße
width = 200
height = 200
buffer_length = width * height
buffer = [10] * buffer_length * 3

# Definition der Kiste (am Ursprung)
cube = [
    [1.0, 1.0, -1.0],
    [1.0, -1.0, -1.0],
    [1.0, 1.0, 1.0],
    [1.0, -1.0, 1.0],
    [-1.0, 1.0, -1.0],
    [-1.0, -1.0, -1.0],
    [-1.0, 1.0, 1.0],
    [-1.0, -1.0, 1.0]
]

# Keine Translation, da die Kiste am Ursprung liegt
translation = [
    [1, 0, 0, 0],
    [0, 1, 0, 0],
    [0, 0, 1, 0],
    [0, 0, 0, 1]
]

# Anzahl der Frames
frames = 50

# Hauptschleife zur Erstellung der Bildsequenz
for t in range(0, frames):
    # Buffer zurücksetzen
    buffer = [10] * buffer_length * 3

    # Rotation berechnen
    rotation = m3_to_m4(rot_x((360 / frames) * t))

    # Transformation kombinieren
    combined = m4_x_m4(rotation, translation)

    # Punkte der Kiste transformieren und auf den Bildschirm projizieren
    for v in cube:
        v_transformed = mult_vec3_m4(v, combined)
        # Perspektivische Division
        screen_space_point = perspective_divide(v_transformed, -1)
        # In Rasterkoordinaten umwandeln
        raster_point = view_to_raster(screen_space_point, width, height)
        # Punkt in den Buffer schreiben
        set_raster_coordinate(raster_point[0], raster_point[1], 200, 200, 0)

    # Frame speichern
    save_ppm(width, height, buffer, t)