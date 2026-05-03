import os


def renombrar_archivos_en_lote(carpeta, prefijo):
    # Verificamos que la carpeta exista antes de hacer nada
    if not os.path.exists(carpeta):
        print(f"Error: La carpeta '{carpeta}' no existe.")
        return

    # Obtenemos solo los archivos (ignorando subcarpetas si las hubiera)
    archivos = [
        f for f in os.listdir(carpeta) if os.path.isfile(os.path.join(carpeta, f))
    ]

    # Ordenamos la lista para que el renombrado sea secuencial según como los exportó Krita
    archivos.sort()

    contador = 1
    for archivo in archivos:
        # Extraemos la extensión original (.jpg, .png, etc.) para conservarla
        _, extension = os.path.splitext(archivo)

        # Armamos el nuevo nombre (ej: autorizado_01.jpg)
        # El :02d asegura que los números menores a 10 tengan un cero a la izquierda
        nuevo_nombre = f"{prefijo}_{contador:02d}{extension}"

        ruta_vieja = os.path.join(carpeta, archivo)
        ruta_nueva = os.path.join(carpeta, nuevo_nombre)

        # Renombramos el archivo
        os.rename(ruta_vieja, ruta_nueva)
        contador += 1

    print(f"¡Listo! Se renombraron {contador - 1} archivos en la carpeta '{carpeta}'.")


# --- Ejecución ---
# Asegúrate de que estas rutas sean las correctas (o cambia a "./dataset/autorizado" si están ahí)
carpeta_autorizado = "./autorizado"
carpeta_no_autorizado = "./no_autorizado"

renombrar_archivos_en_lote(carpeta_autorizado, "autorizado")
renombrar_archivos_en_lote(carpeta_no_autorizado, "no_autorizado")
