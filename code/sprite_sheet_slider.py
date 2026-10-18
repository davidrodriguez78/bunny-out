"""
Sprite Sheet Slicer
===================
Script para dividir sprite sheets en imágenes/frames individuales.

:Author: Enrique Barros Fernández
:License: MIT License
:Copyright: (c) 2026 Enrique Barros Fernández

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
"""

import os
from PIL import Image

# ==========================================
# CONFIGURACIÓN
# ==========================================
# Carpeta donde están los sprite sheets ('.' significa el directorio actual)
INPUT_DIR = "./sprites_input"
# Carpeta donde se guardarán los recortes
OUTPUT_DIR = "./sprites_output"

# Define cuántas filas y columnas tiene la matriz de tu sprite sheet
COLUMNS = 2  # Número de frames en horizontal
ROWS = 1     # Número de frames en vertical

# Extensiones de imagen soportadas
EXTENSIONS = (".png", ".jpg", ".jpeg", ".webp")
# ==========================================


def process_sprite_sheet(filepath, output_folder, columns, rows):
    """Abre un sprite sheet, lo divide en sectores y guarda cada frame."""
    filename = os.path.basename(filepath)
    name_without_ext, _ = os.path.splitext(filename)

    try:
        with Image.open(filepath) as img:
            sheet_width, sheet_height = img.size

            # Calculamos el tamaño de cada frame individual
            frame_width = sheet_width // columns
            frame_height = sheet_height // rows

            # Crear subcarpeta para cada sprite sheet procesado
            sprite_output_dir = os.path.join(output_folder, name_without_ext)
            os.makedirs(sprite_output_dir, exist_ok=True)

            frame_count = 0

            # Recorrido fila por fila (de arriba a abajo) y columna por columna (izquierda a derecha)
            for row in range(rows):
                for col in range(columns):
                    # Coordenadas de corte (left, top, right, bottom)
                    left = col * frame_width
                    top = row * frame_height
                    right = left + frame_width
                    bottom = top + frame_height

                    # Recortar el frame
                    frame = img.crop((left, top, right, bottom))

                    # Guardar el frame individual
                    frame_name = f"frame_{frame_count:03d}.png"
                    frame_path = os.path.join(sprite_output_dir, frame_name)
                    frame.save(frame_path)

                    frame_count += 1

            print(f"✓ Procesado '{filename}': {frame_count} frames guardados en '{sprite_output_dir}'.")

    except Exception as e:
        print(f"✗ Error al procesar '{filename}': {e}")


def main():
    # Crear carpeta de salida si no existe
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    # Si la carpeta de entrada no existe, crearla para comodidad del usuario
    if not os.path.exists(INPUT_DIR):
        os.makedirs(INPUT_DIR)
        print(f"Se ha creado la carpeta '{INPUT_DIR}'. Por favor, coloca allí tus sprite sheets y vuelve a ejecutar.")
        return

    # Buscar todos los archivos compatibles en la carpeta de entrada
    files = [f for f in os.listdir(INPUT_DIR) if f.lower().endswith(EXTENSIONS)]

    if not files:
        print(f"No se encontraron imágenes en '{INPUT_DIR}'.")
        return

    print(f"Encontradas {len(files)} imágenes. Iniciando recorte ({COLUMNS}x{ROWS})...\n")

    for file in files:
        file_path = os.path.join(INPUT_DIR, file)
        process_sprite_sheet(file_path, OUTPUT_DIR, COLUMNS, ROWS)

    print("\n¡Proceso completado!")


if __name__ == "__main__":
    main()