import sys
import time
import math
import os

def calc_media(datos):
    if not datos:
        return 0
    total = 0
    for x in datos:
        total += x
    return total / len(datos)

def calc_mediana(datos):
    if not datos:
        return 0
    datos_ordenados = sorted(datos)
    n = len(datos_ordenados)
    if n % 2 == 0:
        mediana = (datos_ordenados[n // 2 - 1] + datos_ordenados[n // 2]) / 2
    else:
        mediana = datos_ordenados[n // 2]
    return mediana

def calc_moda(datos):
    if not datos:
        return []
    conteo = {}
    for x in datos:
        conteo[x] = conteo.get(x, 0) + 1
    max_conteo = 0
    modas = []
    for x, conteo in conteo.items():
        if conteo > max_conteo:
            max_conteo = conteo
            modas = [x]
        elif conteo == max_conteo:
            modas.append(x)
    return modas

def calc_varianza(datos):
    if not datos:
        return 0
    media = calc_media(datos)
    diferencias_cuadradas = [(x - media) ** 2 for x in datos]
    return calc_media(diferencias_cuadradas)

def calc_desv_estandar(varianza):
    return math.sqrt(varianza)

def extr_dat(nombre_archivo):
    datos = []
    errores = []
    try:
        with open(nombre_archivo, 'r') as f:
            for linea in f:
                try:
                    num = float(linea.strip())
                    datos.append(num)
                except ValueError:
                    errores.append(linea.strip())
    except FileNotFoundError:
        print(f"Error: Archivo '{nombre_archivo}' no encontrado.")
        return None, None

    if errores:
        print("Datos inválidos encontrados en el archivo:")
        for error in errores:
            print(f"- {error}")

    if not datos:
      return None, None

    media = calc_media(datos)
    mediana = calc_mediana(datos)
    moda = calc_moda(datos)
    varianza = calc_varianza(datos)
    desviacion_estandar = calc_desv_estandar(varianza)

    return {
        "media": media,
        "mediana": mediana,
        "moda": moda,
        "varianza": varianza,
        "desviacion_estandar": desviacion_estandar
    }, errores

def escribir_resultados_y_archivo(resultados, nombre_archivo, tiempo_transcurrido):
    version = 1
    nombre_base, extension = os.path.splitext(nombre_archivo)  
    while os.path.exists(nombre_archivo):
        nombre_archivo = f"{nombre_base}_v{version}{extension}"
        version += 1
    try:
        with open(nombre_archivo, 'w') as f:
            f.write(f"Estadísticas Descriptivas:\n")
            for estadistica, valor in resultados.items():
                f.write(f"{estadistica.capitalize()}: {valor}\n")
            f.write(f"Tiempo Transcurrido: {tiempo_transcurrido:.6f} segundos\n")

        print("\nEstadísticas Descriptivas:")
        for estadistica, valor in resultados.items():
            print(f"{estadistica.capitalize()}: {valor}")
        print(f"Tiempo Transcurrido: {tiempo_transcurrido:.6f} segundos")

    except Exception as e:
        print(f"Error al escribir los resultados en el archivo: {e}")


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python computeStatistics.py archivoConDatos.txt")
        sys.exit(1)

    nombre_archivo = sys.argv[1]

    tiempo_inicio = time.time()
    resultados, errores = extr_dat(nombre_archivo)

    if resultados:
        tiempo_fin = time.time()
        tiempo_transcurrido = tiempo_fin - tiempo_inicio
        escribir_resultados_y_archivo(resultados, "EstadisticosResultados.txt", tiempo_transcurrido)