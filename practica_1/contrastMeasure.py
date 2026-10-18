from typing import Protocol
import numpy as np
import cv2


class ContrastMeasure(Protocol):

    def __call__(self, *args) -> float: ...



class Entropia(ContrastMeasure):
        def __call__(self, *args) -> float:
            if args[0] is None:
                raise ValueError("debes pasar la imagen")
            img = args[0]
            histograma = cv2.calcHist(
                [img.astype(np.float32)],
                [0],
                None,
                [256], # en rango de lectura original,
                [0, 1.000001] # se deja el .00001 para incluri al 1
            )

            # convertimos las frencuencias en probabilidades

            probabilidades = histograma.ravel() / img.size

            probabilidades = probabilidades[probabilidades > 0]

            return float(- np.sum(probabilidades * np.log2(probabilidades)))



class Sobel(ContrastMeasure):
    def __call__(self, *args) -> float:
        if args[0] is None:
            raise ValueError("debes pasar la imagen")

        img = args[0]
        gx = cv2.Sobel(img,cv2.CV_64F,1,0,ksize=3)
        gy = cv2.Sobel(img,cv2.CV_64F,0,1,ksize=3)
        magnitud = cv2.magnitude(gx,gy)
        return float(np.mean(magnitud))

