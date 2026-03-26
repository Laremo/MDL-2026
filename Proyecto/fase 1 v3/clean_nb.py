import nbformat

# Nombres de tus archivos
archivo_original = 'Fase1_Firmas_Cheques_OffLine_v3.ipynb'
archivo_limpio = 'Fase1_Firmas_Cheques_OffLine_v3_limpio.ipynb'

# Cargar el notebook original
with open(archivo_original, 'r', encoding='utf-8') as f:
    nb = nbformat.read(f, as_version=4)

# 1. Eliminar la metadata corrupta de los widgets a nivel del notebook
if 'widgets' in nb.metadata:
    del nb.metadata['widgets']

# 2. Revisar y limpiar la metadata a nivel de cada celda por precaución
for cell in nb.cells:
    if getattr(cell, 'metadata', None) and 'widgets' in cell.metadata:
        del cell.metadata['widgets']

# Guardar la nueva versión limpia
with open(archivo_limpio, 'w', encoding='utf-8') as f:
    nbformat.write(nb, f)

print(f"¡Éxito! Se ha guardado una copia limpia sin tocar los outputs: {archivo_limpio}")