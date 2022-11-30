import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 1
options.parallel = 1
matrix = RGBMatrix(options=options)
try:
    image = Image.open("neut.png")
    while(True):
        image.thumbnail((matrix.width, matrix.height + 1), Image.ANTIALIAS)
        matrix.SetImage(image.convert('RGB'))
        if controller.face_number == 0:
            image = Image.open("caution.bmp")
        elif controller.face_number == 1:
            image = Image.open("Grin.png")
        elif controller.face_number == 2:
            image = Image.open("neut.png")
        elif controller.face_number == 3:
            image = Image.open("Sad.png")
        elif controller.face_number == 4:
            image = Image.open("Surprise.png")
        elif controller.face_number == 5:
            image = Image.open("thumbs.png")
        else:
            image = Image.open("caution.bmp")
        image.thumbnail((matrix.width, matrix.height + 1), Image.ANTIALIAS)
        matrix.SetImage(image.convert('RGB'))
except:
    pass