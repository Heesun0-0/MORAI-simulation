#! /usr/bin/env python3

import rospy
import math
from std_msgs.msg import String

import numpy as np

class temp_node:
    __slots__ = ['pub_msg', 'num']
    def __init__(self):
        self.pub_msg = rospy.Publisher("/message", String, queue_size=5)
        self.num = 0

    def send(self):
        self.pub_msg.publish(f"Hello World {self.num}")
        self.num += 1

if __name__ == '__main__':
    rospy.init_node('sender')
    tn = temp_node()
    rate = rospy.Rate(3)
    while not rospy.is_shutdown():
        tn.send()
        rate.sleep()
    