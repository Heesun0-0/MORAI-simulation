#! /usr/bin/python3

import rospy
import math
from sensor_msgs.msg import LaserScan, PointCloud
from geometry_msgs.msg import Point32

import numpy as np
import math


class pcl_processor:
    def __init__(self):
        self.pub_pointcloud = rospy.Publisher(
            "/sample_pointcloud",
            PointCloud,
            queue_size=5
        )
        self.sub_sample = rospy.Subscriber(
            "/sample_scan",
            LaserScan,
            callback=self.convert
        )

    def convert(self, _ls):
        _pc = PointCloud()
        _pc.header.frame_id = "laser"
        
        angle = _ls.angle_min
        _offset = _ls.angle_increment

        for _dis in _ls.ranges:
            _p = Point32()
            _p.x = _dis * math.cos(angle)
            _p.y = _dis * math.sin(angle)
            _p.z = 0.1
            _pc.points.append(_p)
            angle += _offset

        self.pub_pointcloud.publish(_pc)
        

if __name__ == "__main__":
    rospy.init_node("converter", anonymous=False)
    pp = pcl_processor()
    rospy.spin()
