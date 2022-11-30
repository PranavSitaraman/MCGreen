!/usr/bin/python3
import rospy
import RPi.GPIO as GPIO
import time
import sys

from rgbmatrix import RGBMatrix, RGBMatrixOptions
from PIL import Image

from mcgreen_control.msg import Int16

class Face_Controller:
    FACE_TOPIC = "/facial_expression"

    def __init__(self):
        self.tog_sub = rospy.Subscriber(self.FACE_TOPIC, Int16, self.face_callback)
        self.face_number = 2
        self.current_face = -1


    # Called when the face matrix must be changed
    def face_callback(self, data):
        face_number = data.data



if __name__ == "__main__":

    # Configuration for the matrix
    options = RGBMatrixOptions()
    options.rows = 32
    options.cols = 32
    options.chain_length = 1
    options.parallel = 1
    matrix = RGBMatrix(options=options)

    try:
        rospy.init_node("Face_Controller")
        controller = Face_Controller()

        image = Image.open("neut.png")
        while(True):

            if controller.current_face == controller.face_number:
                image.thumbnail((matrix.width, matrix.height + 1), Image.ANTIALIAS)
                matrix.SetImage(image.convert('RGB'))
            else:
                controller.current_face = controller.face_number

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
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
