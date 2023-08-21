#!/usr/bin/env python3

import rospy
from sensor_msgs.msg import PointCloud
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Point32
import math

class MinimalSubscriber:

    def __init__(self):
        rospy.init_node('pointcloud_sphere')
        self.subscription = rospy.Subscriber('scan_data', LaserScan, self.listener_callback)
        self.publisher_ = rospy.Publisher('point_data', PointCloud, queue_size=10)

    def listener_callback(self, msg):
        pc_ = PointCloud()

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
                pc_.points.append(_p)
                
        pc_.header.frame_id = "laser_link"
        self.publisher_.publish(pc_)

def main():
    minimal_subscriber = MinimalSubscriber()
    rospy.spin()

if __name__ == '__main__':
    main()
