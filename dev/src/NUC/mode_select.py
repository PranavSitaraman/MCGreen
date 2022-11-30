#!/usr/bin/python3
import rospy
import numpy as np
from mcgreen_control.msg import Remote, Array
from std_msgs.msg import Int16

class Mode_Selector:
    RECEIVER_TOPIC = "/receiver"
    UPPER_TOPIC = "/remote_upper"
    LOWER_TOPIC = "/remote_lower"
    GAME_TOPIC = "/game_motors"
    MODE_FEEDBACK_TOPIC = "/mode_status"
    UP_DOWN_FEEDBACK_TOPIC = "/up_down_status"
    SENSOR_OVERRIDE_FEEDBACK_TOPIC = "/override_status"

    def __init__(self):
        self.rec_sub = rospy.Subscriber(self.RECEIVER_TOPIC, Remote, self.rec_update)
        self.game_sub = rospy.Subscriber(self.GAME_TOPIC, Array, self.game_update)
        self.upper_safety_pub = rospy.Publisher(self.UPPER_TOPIC, Array, queue_size = 1)
        self.lower_safety_pub = rospy.Publisher(self.LOWER_TOPIC, Array, queue_size = 1)
        self.mode_feedback_pub = rospy.Publisher(self.MODE_FEEDBACK_TOPIC, Int16, queue_size = 1)
        self.up_down_feedback_pub = rospy.Publisher(self.UP_DOWN_FEEDBACK_TOPIC, Int16, queue_size = 1)
        self.sensor_override_feedback_pub = rospy.Publisher(self.SENSOR_OVERRIDE_FEEDBACK_TOPIC, Int16, queue_size = 1)

        self.joystick_rockers = [1500] * 6
        self.mode = 1 #1 is normal 2 arms and legs are disabled 3 is everything
        self.up_down = 1
        self.sensor_override = 1
        self.reset = 0
        self.game_data = [90] * 2

        self.m_feedback = Int16()
        self.m_feedback.data = 1
        self.ud_feedback = Int16()
        self.ud_feedback.data = 1
        self.sensor_feedback = Int16()
        self.sensor_feedback.data = 0

        self.out_upper = Array()
        self.out_upper.arr = [0] * 2 + [90] * 2
        self.out_lower = Array()
        self.out_lower.arr = [1500]*4

        self.mode_feedback_pub.publish(self.m_feedback)
        self.up_down_feedback_pub.publish(self.ud_feedback)
        self.sensor_override_feedback_pub.publish(self.sensor_feedback)

    def rec_update(self,data):
        try:
            self.mode = data.ts[0]/500 - 1
            self.up_down = data.ts[1]/1000 - 1
            self.reset = data.ts[4]/2000
            self.sensor_override = data.ts[5]/2000
            self.joystick_rockers = list(data.xy) + list(data.ts[2:4]) #get arm data
            self.update()
        except:
            pass

    def game_update (self, data):
        self.game_data = data.arr
        self.update()

    def update(self):
        upper_data = [0] * 2 + [90] * 2
        lower_data = [1500] * 4
        #up_down == 1 -> control drivetrain
        #up_down == 0 -> control head/face
        if self.mode == 1:
            if self.up_down == 1:
                lower_data = list(self.joystick_rockers[0:4])
                upper_data[2] = self.out_upper.arr[2]
                upper_data[3] = self.out_upper.arr[3] #keep the head in the position it currently it is
            if self.up_down == 0:#rockers
                if (self.joystick_rockers[4] > 1750):
                    upper_data[0] = 1
                if (self.joystick_rockers[4] < 1250):
                    upper_data[0] = -1
                if (self.joystick_rockers[5] > 1750):
                    upper_data[1] = 1
                if (self.joystick_rockers[5] < 1250):
                    upper_data[1] = -1
                #convert values (index of receiver_joystick) from 1000-2000 range to 0-180 range
                upper_data[2] = int((self.joystick_rockers[0] - 1000) / 1000 * 180)
                upper_data[3] = int((self.joystick_rockers[1] - 1000) / 1000 * 180)

        if self.mode == 2:
            upper_data = [0,0] + self.game_data
            if self.up_down == 1:
                lower_data = list(self.joystick_rockers[0:4])

        if self.mode == 3:
            upper_data = [0,0,90,90]
            lower_data = [1500,1500,1500,1500]

        if self.reset == 1:
            upper_data = [0,0,90,90]
            lower_data = [1500,1500,1500,1500]

        if self.m_feedback.data != self.mode:
            self.m_feedback.data = int(self.mode)
            self.mode_feedback_pub.publish(self.m_feedback)

        if self.ud_feedback.data != self.up_down:
            self.ud_feedback.data = int(self.up_down)
            self.up_down_feedback_pub.publish(self.ud_feedback)

        if self.sensor_feedback.data != self.sensor_override:
            self.sensor_feedback.data = int(self.sensor_override)
            self.sensor_override_feedback_pub.publish(self.sensor_feedback)

        for i in range(0,len(upper_data)):
            upper_data[i] = int(upper_data[i])
        for i in range(0,len(lower_data)):
            lower_data[i] = int(lower_data[i])

        self.out_upper.arr = upper_data
        self.out_lower.arr = lower_data
        self.upper_safety_pub.publish(self.out_upper)
        self.lower_safety_pub.publish(self.out_lower)

if __name__ == "__main__":
    try:
        rospy.init_node("mode_select")
        mode = Mode_Selector()
        rospy.spin()
    except KeyboardInterrupt:
        pass
    except rospy.ROSInterruptException:
        pass
