import time
import sys
from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image
Value = 5
image = Image.open("caution.bmp")
if Value == 0:
	image = Image.open("caution.bmp")
elif Value == 1:
	image = Image.open("Grin.png")
elif Value == 2:
	image = Image.open("neut.png")
elif Value == 3:
	image = Image.open("Sad.png")
elif Value == 4:
	image = Image.open("Surprise.png")
elif Value == 5:
	image = Image.open("thumbs.png")
options = RGBMatrixOptions()
options.rows = 32
options.cols = 32
options.chain_length = 1
options.parallel = 1
matrix = RGBMatrix(options=options)
image.thumbnail((matrix.width, matrix.height + 1), Image.ANTIALIAS)
matrix.SetImage(image.convert('RGB'))
time.sleep(2)
try:
    print("Press CTRL-C to stop.")
    while True:
        time.sleep(100)
except KeyboardInterrupt:
    sys.exit(0)