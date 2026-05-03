import cv2
import numpy as np
import os

def extraer_huellas_por_mancha(input_folder, output_base):
    out_autorizado = os.path.join(output_base, "autorizado")
    out_no_autorizado = os.path.join(output_base, "no_autorizado")

    os.makedirs(out_autorizado, exist_ok=True)
    os.makedirs(out_no_autorizado, exist_ok=True)

    count_total = 0

    for filename in os.listdir(input_folder):
        if not filename.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp')):
            continue

        filepath = os.path.join(input_folder, filename)
        img = cv2.imread(filepath)
        if img is None:
            continue

        if "no_autorizado" in filename.lower():
            save_dir = out_no_autorizado
        elif "autorizado" in filename.lower():
            save_dir = out_autorizado
        else:
            continue

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        # 1. Aplicar un difuminado fuerte
        # Esto elimina el ruido fino (como las líneas de la cuadrícula) 
        # y fusiona las crestas de la huella en una sola masa gris.
        blurred = cv2.GaussianBlur(gray, (55, 55), 0)

        # 2. Binarización adaptativa de las manchas
        # Extrae las manchas oscuras sobre el fondo claro
        thresh = cv2.adaptiveThreshold(
            blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 91, 5
        )

        # 3. Dilatación para consolidar la huella en un bloque sólido
        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
        dilated = cv2.dilate(thresh, kernel, iterations=2)

        # 4. Encontrar contornos de las huellas
        cnts, _ = cv2.findContours(dilated, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

        boxes = []
        for c in cnts:
            x, y, w, h = cv2.boundingRect(c)
            area = w * h
            
            # Filtramos por área para ignorar basuritas o el borde de la hoja.
            # Una huella promedio en estas fotos debería tener dimensiones considerables.
            if 15000 < area < 500000:  
                # Solo tomamos contornos que no sean demasiado alargados (como una línea suelta)
                aspect_ratio = w / float(h)
                if 0.3 < aspect_ratio < 3.0:
                    boxes.append((x, y, w, h))

        if not boxes:
            print(f"Advertencia: No se detectaron huellas en {filename}")
            continue

        # 5. Ordenar de arriba a abajo y luego de izquierda a derecha (Algoritmo de clustering)
        boxes.sort(key=lambda b: b[1])
        filas = []
        fila_actual = [boxes[0]]
        
        for b in boxes[1:]:
            # Margen de tolerancia vertical para considerar que están en la misma fila
            if abs(b[1] - fila_actual[-1][1]) < (b[3] / 2):
                fila_actual.append(b)
            else:
                fila_actual.sort(key=lambda x: x[0])
                filas.append(fila_actual)
                fila_actual = [b]
        
        fila_actual.sort(key=lambda x: x[0])
        filas.append(fila_actual)

        boxes_ordenados = [b for fila in filas for b in fila]
        base_name = os.path.splitext(filename)[0]

        # 6. Recortar aplicando un margen holgado (padding)
        img_h, img_w = gray.shape
        padding = 40  # Ajustar si quieres más o menos espacio blanco alrededor de la huella
        
        for i, (x, y, w, h) in enumerate(boxes_ordenados):
            x1 = max(0, x - padding)
            y1 = max(0, y - padding)
            x2 = min(img_w, x + w + padding)
            y2 = min(img_h, y + h + padding)
            
            roi = img[y1:y2, x1:x2]
            
            if roi.size > 0:
                out_filename = f"{base_name}_huella{i+1}.jpg"
                cv2.imwrite(os.path.join(save_dir, out_filename), roi)
                count_total += 1

        print(f"Se extrajeron {len(boxes_ordenados)} huellas de {filename}")

    print(f"\nProceso terminado. Se extrajeron {count_total} recortes en total.")

input_folder = "./fotos_originales"
output_folder = "./dataset"
extraer_huellas_por_mancha(input_folder, output_folder)