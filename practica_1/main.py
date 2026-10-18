import time
from pathlib import Path

import cv2
import numpy as np
from PIL.ImageEnhance import Contrast

from contrastMeasure import Entropia, Sobel
from geneticoReal import GeneticoReal
from objective_function import Sigmoide


def open_image(path: str):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError
    # normalizamos la imagen
    return img.astype(np.float64) / 255


def main(
    image_path: str,
    measurement_method: str,
    parametros: dict[str, int | float],
    output: str,
) -> str:
    try:
        print("iniciamos transformacion de imagen")
        img = open_image(image_path)

        if measurement_method == "entropia":
            measure = Entropia()
        else:
            measure = Sobel()

        fo = Sigmoide(img, measure)

        b = GeneticoReal(
            fo,
            parametros["Epochs"],
            parametros["N"],
            parametros["Nc"],
            parametros["Pc"],
            parametros["Pm"],
            parametros["Nm"],
        )

        b.run()

        mejor_alpha, mejor_delta = b.get_mejor_individuo()


        best_img = fo.transformar(mejor_alpha, mejor_delta)

        # convertitimos la imagen transformada de nuevo de un rango de 0 a 1 a 0 a 255

        img_tosave = np.round(best_img * 255).astype(np.uint8)

        timestamp = int(time.time())

        output_path = Path(output)
        output_path.mkdir(parents=True, exist_ok=True)
        img_mejorada_path = output_path / f"imagen_mejorada_{timestamp}.png"

        if not cv2.imwrite(str(img_mejorada_path), img_tosave):
            raise OSError(f"No se pudo guardar la imagen en {img_mejorada_path}")

        return str(img_mejorada_path)

    except Exception as e:
        print(e)
        raise
