import cv2
import numpy as np


def open_image(path: str):
    img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)
    if img is None:
        raise FileNotFoundError
    # normalizamos la imagen
    return img.astype(np.floa64) / 255





def main():
    pass

if __name__ == "__main__":
    main()
