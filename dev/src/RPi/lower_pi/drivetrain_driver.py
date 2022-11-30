#!/usr/bin/python3
import rospy
import RPi.GPIO as GPIO
import time
from mcgreen_control.msg import Array

class Head_Servo_Driver:
	MOTOR_TOPIC = "/lower_motors"

	def __init__ (self, LIN1, LIN2, LPWM, RIN1, RIN2, RPWM, threshold):
		self.motor_sub = rospy.Subscriber(self.MOTOR_TOPIC, Array, self.motor_callback)
		self.side = side
		self.LIN1 = LIN1
		self.LIN2 = LIN2
		self.LPWM = LPWM
		self.RIN1 = RIN1
		self.RIN2 = RIN2
		self.RPWM = RPWM
		self.threshold = threshold

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BOARD)
		GPIO.setup(self.LIN1,GPIO.OUT)
		GPIO.setup(self.LIN2,GPIO.OUT)
		GPIO.setup(self.RIN1,GPIO.OUT)
		GPIO.setup(self.RIN2,GPIO.OUT)
		GPIO.output(self.LIN1, False)
		GPIO.output(self.LIN2, False)
		GPIO.output(self.RIN1, False)
		GPIO.output(self.RIN2, False)

		GPIO.setup(self.LPWM,GPIO.OUT)
		self.LPWM_Controller = GPIO.PWM(self.LPWM,50)
		self.LPWM_Controller.start(0)

		GPIO.setup(self.RPWM,GPIO.OUT)
		self.RPWM_Controller = GPIO.PWM(self.RPWM,50)
		self.RPWM_Controller.start(0)

	def motor_callback(self, data):
		# Motor Controls
		# IN1 = 0, IN2 = 0 -> Brake regardless of PWM
		# IN1 = 0, IN2 = 1 -> Reverse Speed @ PWM
		# IN1 = 1, IN2 = 0 -> Forward Speed @ PWM

		left_joy = data.arr[1] # left value (1000-2000)
		right_joy = data.arr[2] # right value (1000-2000)

		# left motor
		if(1500 - self.threshold <= left_joy && 1500 + self.threshold >= left_joy):
			GPIO.output(self.LIN1, False)
			GPIO.output(self.LIN2, False)
		elif(left_joy <= 1500 - self.threshold):
			pwm = 100 - int((left_joy - 1000)*100/(500 - self.threshold)) # manipulation to condense left_joy value into an integer range from 0-100 (test using boundary values of 1000 & 1500-threshold)
			self.LPWM_Controller.ChangeDutyCycle(pwm) # change pwm
			GPIO.output(self.LIN1, False)
			GPIO.output(self.LIN2, True)
		elif(left_joy >= 1500 + self.threshold):
			pwm = int((left_joy - 1500 - self.threshold)*100/(500 - self.threshold)) # manipulation to condense left_joy value into an integer range from 0-100 (test using boundary values of 1500+threshold & 2000)
			self.LPWM_Controller.ChangeDutyCycle(pwm) # change pwm
			GPIO.output(self.LIN1, True)
			GPIO.output(self.LIN2, False)

		# right motor
		if(1500 - self.threshold <= right_joy && 1500 + self.threshold >= right_joy):
			GPIO.output(self.RIN1, False)
			GPIO.output(self.RIN2, False)
		elif(right_joy <= 1500 - self.threshold):
			pwm = 100 - int((right_joy - 1000)*100/(500 - self.threshold)) # manipulation to condense right_joy value into an integer range from 0-100 (test using boundary values of 1000 & 1500-threshold)
			self.RPWM_Controller.ChangeDutyCycle(pwm) # change pwm
			GPIO.output(self.RIN1, False)
			GPIO.output(self.RIN2, True)
		elif(right_joy >= 1500 + self.threshold):
			pwm = int((right_joy - 1500 - self.threshold)*100/(500 - self.threshold)) # manipulation to condense right_joy value into an integer range from 0-100 (test using boundary values of 1500+threshold & 2000)
			self.RPWM_Controller.ChangeDutyCycle(pwm) # change pwm
			GPIO.output(self.RIN1, True)
			GPIO.output(self.RIN2, False)

if __name__ == "__main__":
	try:
		rospy.init_node("Drivetrain_Driver")
		args = {"LIN1": rospy.get_param("~LIN1"), "LIN2": rospy.get_param("~LIN2"), "LPWM": rospy.get_param("~LPWM"), "RIN1": rospy.get_param("~RIN1"), "RIN2": rospy.get_param("~RIN2"), "RPWM": rospy.get_param("~RPWM"), "threshold": rospy.get_param("threshold_joystick")}
		controller = Drivetrain_Driver(args["LIN1"], args["LIN2"], args["LPWM"], args["RIN1"], args["RIN2"], args["RPWM"], args["threshold"])
		rospy.spin()
	except KeyboardInterrupt:
		pass
	except rospy.ROSInterruptException:
		pass
