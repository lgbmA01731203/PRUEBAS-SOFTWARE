"""
Conviertir números de un archivo a binario y hexadecimal.
"""

import sys
import time
import os

def decimal_a_binario(n):
    """Convierte un número decimal a binario"""
    if n == 0:
        return "0"
    binario = ""
    while n > 0:
        binario = str(n % 2) + binario
        n //= 2
    return binario

def decimal_a_hexadecimal(n):
    """Convierte un número decimal a hexadecimal"""
    hexadecimal = ""
    hex_chars = "0123456789ABCDEF"
    if n == 0:
        return "0"
    while n > 0:
        hexadecimal = hex_chars[n % 16] + hexadecimal
        n //= 16
    return hexadecimal

def convertir_numeros(nombre_archivo_entrada):
    """Convierte números a binario y hexadecimal desde un archivo.

    Args:
        nombre_archivo_entrada: Ruta al archivo de entrada.

    Returns:
        Resultados de la conversión y una lista de errores.
    """
    resultados = {}
    errores = []
    try:
        with open(nombre_archivo_entrada, 'r', encoding='utf-8') as f:
            for linea in f:
                try:
                    num = int(linea.strip())  # Intentar convertir a entero primero
                    binario = decimal_a_binario(num)
                    hexadecimal = decimal_a_hexadecimal(num)
                    resultados[num] = {"binario": binario, "hexadecimal": hexadecimal}
                except ValueError:
                    try:
                        num = float(linea.strip()) # Si falla como entero, intentar como float
                        binario = decimal_a_binario(int(num)) # Convertir la parte entera a binario
                        hexadecimal = decimal_a_hexadecimal(int(num)) # Convertir la parte entera a hexadecimal

                        resultados[num] = {"binario": binario, "hexadecimal": hexadecimal}
                    except ValueError:
                        errores.append(linea.strip())

    except FileNotFoundError:
        print(f"Error: Archivo '{nombre_archivo_entrada}' no encontrado.")
        return None, None

    if errores:
        print("Datos inválidos encontrados en el archivo:")
        for error in errores:
            print(f"- {error}")

    return resultados, errores

def Imp_res(resultados, nombre_archivo_salida, tiempo_transcurrido):
    """Escribe los resultados en un archivo, agregando una versión si ya existe.

    Args:
        resultados: Resultados de la conversión.
        nombre_archivo_salida: Ruta al archivo de salida.
        tiempo_transcurrido: Tiempo transcurrido en segundos.
    """
    version = 1
    nombre_base, extension = os.path.splitext(nombre_archivo_salida)
    while os.path.exists(nombre_archivo_salida):
        nombre_archivo_salida = f"{nombre_base}_v{version}{extension}"
        version += 1
    try:
        with open(nombre_archivo_salida, 'w', encoding='utf-8') as f:
            f.write("Resultados de la Conversión:\n")
            for num, conversion in resultados.items():
                f.write(f"Decimal: {num}, Binario: {conversion['binario']}, Hexadecimal: {conversion['hexadecimal']}\n")
            f.write(f"Tiempo Transcurrido: {tiempo_transcurrido:.6f} segundos\n")

        print("\nResultados de la Conversión:")
        for num, conversion in resultados.items():
            print(f"Decimal: {num}, Binario: {conversion['binario']}, Hexadecimal: {conversion['hexadecimal']}")
        print(f"Tiempo Transcurrido: {tiempo_transcurrido:.6f} segundos")

    except Exception as e:
        print(f"Error al escribir los resultados en el archivo: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Uso: python convertNumbers.py archivoConDatos.txt")
        sys.exit(1)

    nombre_archivo = sys.argv[1]

    tiempo_inicio = time.time()
    resultados, errores = convertir_numeros(nombre_archivo)

    if resultados:
        tiempo_fin = time.time()
        tiempo_transcurrido = tiempo_fin - tiempo_inicio
        Imp_res(resultados, "ConversionResults.txt", tiempo_transcurrido)