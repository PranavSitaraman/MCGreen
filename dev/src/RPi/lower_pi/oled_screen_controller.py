#!/usr/bin/python3
import rospy
from std_msgs.msg import Int16, String, Bool
from mcgreen_control.msg import Array
from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1327
from PIL import ImageFont, ImageDraw
from time import sleep
import textwrap

serial = spi(device=0, port=0)
device = ssd1327(serial)
font_size = 12
font_name = "FreeMono.ttf"
font = ImageFont.truetype(font_name, font_size)

class OLED:
	MODE_TOPIC = "/mode_status"
	UP_DOWN_TOPIC =  "/up_down_status"
	SAFETY_TOPIC = "/safety_status"
	FAILSAFE_TOPIC = "/override_status"
	GAME_TOPIC = "/current_game"
	EXPRESSION_TOPIC = "/facial_expression"
	UPPER_TOPIC = "/upper_motors"
	LOWER_TOPIC = "/lower_motors"

	def __init__(self):
		self.mode_sub = rospy.Subscriber(self.MODE_TOPIC, Int16, self.mode_set)
		self.up_down_sub = rospy.Subscriber(self.UP_DOWN_TOPIC, Int16, self.up_down_set)
		self.game_sub = rospy.Subscriber(self.GAME_TOPIC, String, self.game_set)
		self.upper_sub = rospy.Subscriber(self.UPPER_TOPIC, Array, self.upper_set)
		self.lower_sub = rospy.Subscriber(self.LOWER_TOPIC, Array, self.lower_set)
		self.face_sub  = rospy.Subscriber(self.EXPRESSION_TOPIC, Int16, self.face_set)
		self.safety_sub = rospy.Subscriber(self.SAFETY_TOPIC, Bool, self.safety_set)
		self.failsafe_sub = rospy.Subscriber(self.FAILSAFE_TOPIC, Int16, self.failsafe_set)
		self.mode = 1
		self.up_down = 1
		self.fs = 1
		self.game = "None"
		self.face = "Neutral"
		self.upper=[0] * 2 + [90] * 2
		self.lower=[1500] * 4
		self.safe = "SAFE"
		self.line = 0
		self.time = 0

	def mode_set(self, data):
		self.mode = data.data

	def up_down_set(self, data):
		self.up_down = data.data

	def failsafe_set(self, data):
		self.fs = data.data

	def safety_set(self, data):
		if data.data == True:
			self.safe = "SAFE"
		else:
			self.safe = "WARNING"

	def upper_set(self, data):
		self.upper = data.arr

	def lower_set(self, data):
		self.lower = data.arr

	def game_set(self, data):
		self.game = str(data.data)

	def face_set(self, data):
		self.face = data.data
		if self.face == 0:
			self.face = "Warn"
		elif self.face < 4:
			self.face = "Happy " + str(self.face)
		elif self.face > 4:
			self.face = "Sad " + str(self.face)
		else:
			self.face = "Neutral"

	def display(self):
		self.line = 0
		with canvas(device) as draw:
			self.write_text("M: " + str(self.mode) + " U/D: " + str(self.up_down), draw)
			self.write_text("Game: " + self.game, draw)
			self.write_text("Face: " + str(self.face), draw)

			self.write_text("LA: " + str(self.upper[:2]), draw)
			self.write_text("Servo: " + str(self.upper[2:]), draw)

			self.write_text("D_Motors: ", draw)
			self.write_text(str(self.lower[1:3]), draw)

			self.write_text("Status: " + self.safe, draw)
			self.write_text("Sensor Override: " + str(self.fs), draw)

	def write_text(self, text, draw): # if text is too long it returns the text with \n
		w = font.getsize(text)[0]
		h = font.getsize(text)[1]
		line_height = font.getsize("hg")[1]
		length = len(text)
		current_size = 0
		begin = 0
		newlines = 0
		modified_text = ""
		if w <= device.width:
			draw.text((0, self.line), text, font=font, fill="white")
			h = font.getsize(text)[1]
			self.line += line_height
			#return 1
		else:
			for i in range(length):
				current_w = font.getsize(text[begin:i+1])[0]
				current_h = font.getsize(text[begin:i+1])[1]
				if current_w > 128:
					draw.text((0, self.line), text[begin:i], font=font, fill="white")
					h = font.getsize(text[begin:i])[1]
					self.line += line_height
					begin = i
			draw.text((0, self.line), text[begin:length+1], font=font, fill="white")
			h = font.getsize(text[begin:length+1])[1]
			self.line += line_height

if __name__ == "__main__":
	rospy.init_node("OLED_Screen_Controller")
	args = {"rate": rospy.get_param("~rate")}
	screen = OLED()
	r = rospy.Rate(args["rate"])
	while not rospy.is_shutdown():
		screen.display()
		r.sleep()
