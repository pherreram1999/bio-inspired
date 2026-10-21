
from pathlib import Path
from main import main

# Ruta de la imagen original
imagen = r"C:\Users\jazmi\Downloads\Practica_1_Imagenes\imagen3.jpeg"

# Carpeta donde se guardará el resultado
salida = r"C:\Users\jazmi\Downloads\Practica_1_Imagenes\resultados_prueba"

# Método de medición: "entropia" o "sobel"
metodo = "entropia"

# Parámetros que les dieron en el README
parametros = {
    "N": 512,
    "Nc": 2,
    "Pc": 0.7,
    "Pm": 0.02,
    "Nm": 20,
    "Epochs": 15,
}

# Verificar que exista la imagen
if not Path(imagen).is_file():
    raise FileNotFoundError(f"No se encontró la imagen: {imagen}")

print("Iniciando procesamiento...")
print(f"Imagen: {imagen}")
print(f"Método: {metodo}")
print(f"Parámetros: {parametros}")

resultado = main(imagen, metodo, parametros, salida)

print("\nProcesamiento terminado.")
print("Resultado:", resultado)
