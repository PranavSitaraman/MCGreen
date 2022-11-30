#!/usr/bin/python3
import serial
import rospy
from mcgreen_control.msg import Array
from binascii import hexlify

class Remote_Control:
	RECEIVER_TOPIC = "/receiver_output"

	def __init__ (self, rate):
		self.pub = rospy.Publisher(self.RECEIVER_TOPIC, Array, queue_size=1)
		self.rate = rospy.Rate(rate)
		self.out = [1500] * 10
		self.ser = serial.Serial( port='/dev/serial0', baudrate=115200, timeout=1)

	def recieve(self):
		while not rospy.is_shutdown():
			hex = hexlify(self.ser.read(2))
			if hex.decode() == "2040":
				for i in range(10):
					lower_byte = self.ser.read(1)
					upper_byte = self.ser.read(1)
					if hexlify(lower_byte+upper_byte) != "":
						self.out[i] = int(hexlify(upper_byte+lower_byte),16)
			msg = Array()
			msg.arr = self.out
			self.pub.publish(msg)

if __name__ == '__main__':
	try:
		rospy.init_node("Remote_Control_Reciever")
		args = {"rate": rospy.get_param("~rate")}
		controller = Remote_Control(args["rate"])
		controller.recieve()
		rospy.spin()
	except KeyboardInterrupt:
		pass
	except rospy.ROSInterruptException:
		pass
