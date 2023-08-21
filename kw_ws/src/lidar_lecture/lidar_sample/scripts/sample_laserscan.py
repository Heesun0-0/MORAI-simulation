#! /usr/bin/python3

import rospy
import math
from sensor_msgs.msg import LaserScan

import numpy as np
import random


class pcl_processor:
    __slots__ = ['pub_sample']
    def __init__(self):
        self.pub_sample = rospy.Publisher("/sample_scan", LaserScan, queue_size=5)

    def make_one(self):
        ls = LaserScan()
        ls.header.stamp = rospy.Time.now()
        ls.header.frame_id = "laser"

        ls.angle_min = 0.0
        ls.angle_max = 0.1
        ls.angle_increment = 0.1
        ls.time_increment = 0.1
        ls.range_min = 0.0
        ls.range_max = 100
        ls.ranges = [0.5, 2.7]

        self.pub_sample.publish(ls)

    def make_samples(self):
        ls = LaserScan()
        ls.header.stamp = rospy.Time.now()
        ls.header.frame_id = "laser"

        ls.angle_min = -3.14
        ls.angle_max = 3.14
        ls.angle_increment = 6.28 / 360.0
        ls.time_increment = 0.1
        ls.range_min = 0.0
        ls.range_max = 100.0
        ls.ranges = [0.7 for i in range(0, 360)]
        # ls.intensities = [0.1 for i in range(0, 360)]
        # _lt1 = [i * 0.002 for i in range(0, 180)]
        # _lt2 = [(i - 180) * 0.002 for i in range(360, 180, -1)]
        # ls.ranges = _lt1 + _lt2

        self.pub_sample.publish(ls)


if __name__ == "__main__":
    rospy.init_node("sample_laserscan", anonymous=False)
    pp = pcl_processor()
    rate = rospy.Rate(15)
    while not rospy.is_shutdown():
        # pp.make_one()
        pp.make_samples()
        rate.sleep()
