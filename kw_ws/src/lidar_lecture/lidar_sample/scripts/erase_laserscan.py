#! /usr/bin/env python3

import rospy
from sensor_msgs.msg import LaserScan
import numpy as np

class Eraser:
    def __init__(self):
        rospy.init_node("eraser", anonymous=False)
        self.sub_laser = rospy.Subscriber("/scan", LaserScan, callback=self.callback2)
        self.pub_laser = rospy.Publisher("/scan_c", LaserScan, queue_size=5)

    def callback(self, laser):
        _ls = LaserScan()
        _ls.header.frame_id = "scan"
        _ls.angle_increment = laser.angle_increment
        _ls.angle_min = laser.angle_min
        _ls.angle_max = laser.angle_max
        _ls.range_min = laser.range_min
        _ls.range_max = laser.range_max
        
        for i in range(0, len(laser.ranges)):
            if laser.ranges[i] > 2.0:
                _ls.ranges.append(0.0)
            else:
                _ls.ranges.append(laser.ranges[i])
        self.pub_laser.publish(_ls)
    
    def callback2(self, laser):
        laser.range_max = 2.0
        self.pub_laser.publish(laser)

if __name__ == "__main__":
    er = Eraser()
    rospy.spin()
