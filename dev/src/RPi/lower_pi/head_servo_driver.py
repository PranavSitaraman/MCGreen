#!/usr/bin/python3
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Array

class Head_Servo_Driver:
    SERVO_TOPIC = "/upper_motors"

    def __init__(self,vertical,horizontal):
        self.tog_sub = rospy.Subscriber(self.SERVO_TOPIC, Array, self.servo_callback)
        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(vertical,GPIO.OUT)
        GPIO.setup(horizontal, GPIO.OUT)
        self.vertical_controller = GPIO.PWM(vertical,50)
        self.horizontal_controller = GPIO.PWM(horizontal, 50)
        self.vertical_controller.start(0)
        self.horizontal_controller.start(0)

    def servo_callback(self, data):
        horizontal_angle = int(2 + (data.arr[2]/18))#will have to fix once position of servos is determined
        vertical_angle = int(2 + (data.arr[3]/18))#will have to fix once position of servos is determined
        self.vertical_controller.ChangeDutyCycle(vertical_angle)
        self.horizontal_controller.ChangeDutyCycle(horizontal_angle)

    def clean(self):
        self.vertical_controller.ChangeDutyCycle(7)
        self.horizontal_controller.ChangeDutyCycle(7)

if __name__ == "__main__":
    try:
        rospy.init_node("Head_Servo_Driver")
        args = {"vertical": rospy.get_param("~vertical"), "horizontal": rospy.get_param("~horizontal")}
        controller = Head_Servo_Driver(args["vertical"], args["horizontal"])
        rospy.spin()
        rospy.on_shutdown(controller.clean)
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
