#!/usr/bin/python3
import rospy
from mcgreen_control.msg import Remote, Arm, Sensor, Array
from std_msgs.msg import Int16

class Remote_Sensor_Processor:
    RECEIVER_OUTPUT_TOPIC =  "/receiver_output"
    LEFT_TOPIC = "/left_arm_sensor"
    RIGHT_TOPIC = "/right_arm_sensor"
    RECEIVER_TOPIC = "/receiver"
    SENSOR_TOPIC = "/sensor_data"
    initial_ultra=rospy.get_param("Sensors/default_ultra")

    def __init__(self):
        self.rec_sub = rospy.Subscriber(self.RECEIVER_OUTPUT_TOPIC, Array, self.receiver_callback)
        self.left_sub = rospy.Subscriber(self.LEFT_TOPIC, Arm, self.left_arm_callback)
        self.right_sub = rospy.Subscriber(self.RIGHT_TOPIC, Arm, self.right_arm_callback)
        self.rec_pub = rospy.Publisher(self.RECEIVER_TOPIC, Remote, queue_size = 1)
        self.sensor_pub = rospy.Publisher(self.SENSOR_TOPIC, Sensor, queue_size = 1)

        #Intiate variables
        self.sensors = Sensor()
        self.out_receiver = Remote()

        #Arm initial values
        self.left_data=Arm()
        self.left_data.ultrasonic=self.initial_ultra
        self.right_data=Arm()
        self.right_data.ultrasonic=self.initial_ultra
        self.sensors.ultrasonic=[self.initial_ultra]*2

    def right_arm_callback(self, data):
        self.right_data = data
        self.sensors.ultrasonic = [self.left_data.ultrasonic, self.right_data.ultrasonic]

    def left_arm_callback(self, data):
        self.left_data = data
        self.sensors.ultrasonic = [self.left_data.ultrasonic, self.right_data.ultrasonic]

    def receiver_callback(self, data):
        self.receiver_data = data.arr
        self.receiver_splice()

    def receiver_splice(self):
        self.out_receiver.ts = self.receiver_data[4:]
        self.out_receiver.xy = self.receiver_data[3::-1]

    def data_publish(self):
        self.sensor_pub.publish(self.sensors)
        self.rec_pub.publish(self.out_receiver)

if __name__ == "__main__":
    rospy.init_node("remote_control_process")
    args = {"rate": rospy.get_param("~rate")}
    peripheral = Remote_Sensor_Processor()
    r = rospy.Rate(args["rate"])
    while not rospy.is_shutdown():
        peripheral.data_publish()
        r.sleep()
