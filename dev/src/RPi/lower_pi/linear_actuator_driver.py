#!/usr/bin/python3
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Array

class Linear_Actuator_Driver:
    MOTOR_TOPIC = "/upper_motors"

    def __init__ (self, side, IN1, IN2, PWM, PWM_VAL):
        self.motor_sub = rospy.Subscriber(self.MOTOR_TOPIC, Array, self.actuator_callback)
        self.side = side
        self.IN1 = IN1
        self.IN2 = IN2
        self.PWM = PWM
        self.PWM_VAL = PWM_VAL
        if self.side == "left":
            self.index = 0
        else:
            self.index = 1

        GPIO.setwarnings(False)
        GPIO.setmode(GPIO.BOARD)
        GPIO.setup(self.IN1,GPIO.OUT)
        GPIO.setup(self.IN2,GPIO.OUT)
        GPIO.output(self.IN1, False)
        GPIO.output(self.IN2, False)

        GPIO.setup(PWM,GPIO.OUT)
        self.PWM_Controller = GPIO.PWM(self.PWM,50)
        self.PWM_Controller.start(self.PWM_VAL)


    def actuator_callback(self, data):
        motor_command = data.arr[self.index]
        print(motor_command)
        if motor_command == 1:
            GPIO.output(self.IN1, False)
            GPIO.output(self.IN2, True)
        elif motor_command == -1:
            GPIO.output(self.IN1, True)
            GPIO.output(self.IN2, False)
        else:
            GPIO.output(self.IN1, False)
            GPIO.output(self.IN2, False)


if __name__ == "__main__":
    try:
        rospy.init_node("Linear_Actuator_Driver")
        args = {"side": rospy.get_param("~side"), "IN1": rospy.get_param("~IN1"), "IN2": rospy.get_param("~IN2"), "PWM": rospy.get_param("~PWM"), "PWM_VAL": rospy.get_param("~PWM_VAL")}
        actuator = Linear_Actuator_Driver(args["side"], args["IN1"], args["IN2"], args["PWM"], args["PWM_VAL"])
        rospy.spin()
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
