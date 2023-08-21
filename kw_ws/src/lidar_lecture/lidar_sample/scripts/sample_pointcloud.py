#! /usr/bin/env python3

import rospy
import math
from sensor_msgs.msg import PointCloud
from geometry_msgs.msg import Point32

import numpy as np
import random


class pcl_processor:
    __slots__ = ['pub_sample']
    def __init__(self):
        self.pub_sample = rospy.Publisher(
            "/sample_pcl",
            PointCloud,
            queue_size=5
        )

    def sample_run(self):
        _pcl = PointCloud()

        _l = 1.0

        for i in range(0, 628, 10):
            _theta = 3.14 - (i * 0.01)
            _z = _l * math.sin(_theta)
            for j in range(0, 628, 10):
                _theta2 = 3.14 - (j * 0.01)
                _x = _l * math.cos(_theta) * math.cos(_theta2)
                _y = _l * math.cos(_theta) * math.sin(_theta2)

                _p = Point32()
                _p.x = _x
                _p.y = _y
                _p.z = _z
                _pcl.points.append(_p)
        _pcl.header.frame_id = "laser"
        self.pub_sample.publish(_pcl)


if __name__ == "__main__":
    rospy.init_node("sample_laserscan", anonymous=False)
    pp = pcl_processor()
    rate = rospy.Rate(5)
    while not rospy.is_shutdown():
        pp.sample_run()
        rate.sleep()
