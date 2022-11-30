import rospy
from std_msgs.msg import Int16, Bool, String
from mcgreen.msg import Array
import time
import sys
import pygame
from pygame import mixer
import random
import math
import threading
import os
class Display_Controller:
    MODE_TOPIC = "/mode_status"
    FACE_EXPRESSION = "/game_face" 
    HEAD_TOPIC = "/game_motors" 
    GAME_TOPIC = "/current_game" 
    def __init__ (self):
        self.mode_sub = rospy.Subscriber(self.MODE_TOPIC, Int16, self.mode_update)
        self.face_pub=rospy.Publisher(self.FACE_EXPRESSION, Int16, queue_size=1)
        self.head_pub=rospy.Publisher(self.HEAD_TOPIC, Array, queue_size=1)
        self.game_pub=rospy.Publisher(self.GAME_TOPIC, String, queue_size=1)
        self.expression=Int16()
        self.expression.data=4
        self.head=Array()
        self.head.arr=[90,90]
        self.name=String()
        self.name.data = "None"
        self.game_pub.publish(self.name)
        self.head_pub.publish(self.head)
        self.face_pub.publish(self.expression)
        self.current_mode = 3
        self.safety = True
    def mode_update(self, mode):
        self.current_mode = mode.data
    def face_update(self, face):
        self.expression.data = int(face)
        self.face_pub.publish(self.expression)
    def game_update(self, game):
        self.name.data = str(game)
        self.game_pub.publish(self.name)
    def head_update(self, angle):
        self.head.arr = angle
        self.head_pub.publish(self.head)
if __name__=="__main__":
    try:
        rospy.init_node("Display_Controller")
        face_controller = Display_Controller()
        rospy.spin()
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass