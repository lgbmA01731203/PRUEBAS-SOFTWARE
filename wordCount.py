"""
Cuenta la frecuencia de palabras distintas en un archivo de texto.
"""

import sys
import time
import os

def contar_palabras(nombre_archivo_entrada):
    """Cuenteo de palabras distintas en un archivo.

    Args:
        nombre_archivo_entrada: La ruta al archivo de entrada.

    Returns:
     Lista de palabras y sus frecuencias, y una lista de errores.
    """
    conteo_palabras = {}
    errores = []

    try:
        with open(nombre_archivo_entrada, 'r', encoding='utf-8') as f:
            for linea in f:
                palabras = linea.split() 
                for palabra in palabras:
                    palabra = palabra.strip().lower()  
                    if palabra:  
                      if palabra.isalnum(): 
                        conteo_palabras[palabra] = conteo_palabras.get(palabra, 0) + 1
                      else:
                        errores.append(palabra)
    except FileNotFoundError:
        print(f"Error: Archivo '{nombre_archivo_entrada}' no encontrado.")
        return None, None

    if errores:
        print("Datos inválidos encontrados en el archivo:")
        for error in errores:
            print(f"- {error}")

    return conteo_palabras, errores

def escribir_resultados_y_archivo(conteo_palabras, nombre_archivo_salida, tiempo_transcurrido):
    """Escribe los resultados en un archivo, agregando una versión si ya existe.

    Args:
        conteo_palabras: Lista las palabras y sus frecuencias.
        nombre_archivo_salida: La ruta al archivo de salida.
        tiempo_transcurrido: El tiempo transcurrido en segundos.
    """
    version = 1
    nombre_base, extension = os.path.splitext(nombre_archivo_salida)
    while os.path.exists(nombre_archivo_salida):
        nombre_archivo_salida = f"{nombre_base}_v{version}{extension}"
        version += 1

    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
            f.write("Conteo de Palabras:\n")
            for palabra, frecuencia in conteo_palabras.items():
                f.write(f"{palabra}: {frecuencia}\n")
            f.write(f"Tiempo Transcurrido: {tiempo_transcurrido:.6f} segundos\n")

        print("\nConteo de Palabras:")
        for palabra, frecuencia in conteo_palabras.items():
            print(f"{palabra}: {frecuencia}")
        print(f"Tiempo Transcurrido: {tiempo_transcurrido:.6f} segundos")

    except Exception as e:
        print(f"Error al escribir los resultados en el archivo: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python wordCount.py archivoConDatos.txt")
        sys.exit(1)

    nombre_archivo = sys.argv[1]

    tiempo_inicio = time.time()
    conteo_palabras, errores = contar_palabras(nombre_archivo)

    if conteo_palabras:
        tiempo_fin = time.time()
        tiempo_transcurrido = tiempo_fin - tiempo_inicio
        escribir_resultados_y_archivo(conteo_palabras, "WordCountResults.txt", tiempo_transcurrido)