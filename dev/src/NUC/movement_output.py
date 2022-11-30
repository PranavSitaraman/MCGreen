#!/usr/bin/python3
import rospy
from mcgreen_control.msg import Sensor, Array, Remote
from numpy import interp
from std_msgs.msg import Int16, Bool

class Movement_Output:
    TOGGLE_TOPIC="/receiver"
    UPPER_IN = "/remote_upper"
    LOWER_IN = "/remote_lower"
    US_TOPIC = "/sensor_data"
    UPPER_OUT = "/upper_motors"
    LOWER_OUT = "/lower_motors"
    FEEDBACK_TOPIC = "/safety_status"
    FACE_IN = "/game_face"
    FACE_OUT = "/facial_expression"
    OVERRIDE_IN = "/override_status"

    threshold = rospy.get_param("Sensors/threshold_ultra")
    def __init__(self):
        self.upper_safe = Array()
        self.lower_safe = Array()
        self.feedback = Bool()
        self.ultrasonic = [80]*2
        self.feedback.data = True
        self.safe = True
        self.upper = [1500] * 2 + [90] * 2
        self.lower = [1500] * 4
        self.face = Int16()
        self.face.data = 4
        self.override = Int16()
        self.override.data = 1
        self.safety_toggle = False
        self.up_sub = rospy.Subscriber(self.UPPER_IN, Array, self.up_update)
        self.low_sub = rospy.Subscriber(self.LOWER_IN, Array, self.low_update)
        self.sensor_sub = rospy.Subscriber(self.US_TOPIC, Sensor, self.sensor_update)
        self.tog_sub = rospy.Subscriber(self.TOGGLE_TOPIC, Remote, self.toggle_update)
        self.face_sub = rospy.Subscriber(self.FACE_IN, Int16, self.face_update)
        self.override_sub = rospy.Subscriber(self.OVERRIDE_IN, Int16, self.override_update)
        self.face_pub = rospy.Publisher(self.FACE_OUT, Int16, queue_size=1)
        self.upper_pub = rospy.Publisher(self.UPPER_OUT, Array, queue_size = 1)
        self.lower_pub = rospy.Publisher(self.LOWER_OUT, Array, queue_size = 1)
        self.safety_feedback_pub = rospy.Publisher(self.FEEDBACK_TOPIC, Bool, queue_size = 1)
        self.safety_feedback_pub.publish(self.feedback)


    def up_update(self,data):
        self.upper = list(data.arr)

    def low_update(self,data):
        self.lower = list(data.arr)

    def face_update(self,data):
        self.face = data

    def sensor_update(self, data):
        self.ultrasonic = list(data.ultrasonic)

    def toggle_update(self, data):
        try:
            if(data.ts[4] == 2000):
                self.safety_toggle = True
            else:
                self.safety_toggle = False
        except IndexError:
            self.safety_toggle = False

    def override_update(self, data):
        self.override = data

    def update(self):
        # upper_safe = [arm_left, arm_right, head_x, head_y]
        if ((self.ultrasonic[0] < self.threshold or self.ultrasonic[1] < self.threshold) and self.override.data == 0):
            self.lower_safe.arr = [1500]*4
            self.upper_safe.arr = [0]*2 + [90]*2
            self.safe = False

        if (self.safety_toggle == True):
            self.safe = True

        if self.safe == False:
            warn_face = Int16()
            warn_face.data = 0
            self.face_pub.publish(warn_face)
            self.upper_pub.publish(self.upper_safe)
            self.lower_pub.publish(self.lower_safe)

        if self.safe == True:
            self.lower_safe.arr = self.lower
            self.upper_safe.arr = self.upper
            self.face_pub.publish(self.face)
            self.upper_pub.publish(self.upper_safe)
            self.lower_pub.publish(self.lower_safe)

        if self.safe != self.feedback.data:
            self.feedback.data = self.safe
            self.safety_feedback_pub.publish(self.feedback)

if __name__ == "__main__":
    rospy.init_node("Movement_Output")
    args = {"rate": rospy.get_param("~rate")}
    safe = Movement_Output()
    r = rospy.Rate(args["rate"])
    while not rospy.is_shutdown():
        safe.update()
        r.sleep()
