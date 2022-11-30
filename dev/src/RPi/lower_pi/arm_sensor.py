#!/usr/bin/python3
import time as Time
import rospy
from mcgreen_control.msg import Arm
import argparse
import RPi.GPIO as GPIO
import statistics

class Arm_Sensor:

    def __init__(self, topic, trigger, echo):
        self.arm_pub = rospy.Publisher(topic, Arm, queue_size=1)
        self.data = Arm()
        GPIO.setmode(GPIO.BOARD)
        self.GPIO_TRIGGER = trigger
        self.GPIO_ECHO = echo
        self.maxTime = 0.04
        GPIO.setup(self.GPIO_TRIGGER, GPIO.OUT)
        GPIO.setup(self.GPIO_ECHO, GPIO.IN)

    def sense(self):
        GPIO.output(self.GPIO_TRIGGER, False)
        Time.sleep(0.01)
        GPIO.output(self.GPIO_TRIGGER, True)
        Time.sleep(0.00001)
        GPIO.output(self.GPIO_TRIGGER, False)

        StartTime = Time.time()
        timeout = StartTime + self.maxTime

        while GPIO.input(self.GPIO_ECHO) == 0 and StartTime < timeout:
            StartTime = Time.time()

        if (StartTime > timeout):
            distance = self.sense()
            return int(distance)

        StopTime = Time.time()
        timeout = StopTime + self.maxTime

        while GPIO.input(self.GPIO_ECHO) == 1 and StopTime < timeout:
            StopTime = Time.time()

        if (StopTime > timeout):
            distance = self.sense()
            return int(distance)

        TimeElapsed = StopTime - StartTime
        distance = (TimeElapsed * 34300) / 2

        if distance < 2:
            return 400
        elif distance > 400:
            return 400
        else:
            return int(distance)

    def publish(self):
        values = []
        for i in range(3):
            values.append(self.sense())
        distance = statistics.median(values)

        self.data.ultrasonic = int(distance)
        self.arm_pub.publish(self.data)


if __name__ == "__main__":
    rospy.init_node("arm_sensor")
    args = {"topic": rospy.get_param("~topic"), "rate": rospy.get_param("/Sensors/rate"), "trigger": rospy.get_param("~trigger"), "echo": rospy.get_param("~echo")}
    sensor = Arm_Sensor(args["topic"], args["trigger"], args["echo"])
    r = rospy.Rate(args["rate"])
    while not rospy.is_shutdown():
        sensor.publish()
        r.sleep()
    GPIO.cleanup()
