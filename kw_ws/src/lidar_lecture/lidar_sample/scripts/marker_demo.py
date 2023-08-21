#! /usr/bin/python3

import rospy
import math
from sensor_msgs.msg import LaserScan
from visualization_msgs.msg import Marker, MarkerArray

import numpy as np


class pcl_processor:
    __slots__ = ['sub_laser', 'pub_marker']
    def __init__(self):
        self.sub_laser = rospy.Subscriber(
            "/sample_scan",
            LaserScan,
            callback=self.judge
        )
        self.pub_marker = rospy.Publisher(
            "/mk_array",
            MarkerArray,
            queue_size=5
        )

    def judge(self, _ls:LaserScan):
        currentRadian = _ls.angle_min
        _rInc = _ls.angle_increment

        _mkArray = MarkerArray()

        for i in range(0, len(_ls.ranges)):
            x = _ls.ranges[i] * math.cos(currentRadian)
            y = _ls.ranges[i] * math.sin(currentRadian)
            _mkArray.markers.append(
                self.setMarker(
                    (x, y),
                    i,
                    1
                )
            )
            currentRadian += _rInc

        self.pub_marker.publish(_mkArray)

    def setMarker(self, _p, _id, _op):
        marker = Marker()
        marker.header.frame_id = "laser"
        marker.ns = "position"
        marker.id = _id
        marker.lifetime = rospy.Duration.from_sec(0.1)

        marker.type = Marker.SPHERE
        marker.action = Marker.ADD

        marker.pose.position.x = _p[0]
        marker.pose.position.y = _p[1]
        marker.pose.position.z = 0.01

        marker.pose.orientation.x = 0.0
        marker.pose.orientation.y = 0.0
        marker.pose.orientation.z = 0.0
        marker.pose.orientation.w = 1.0

        marker.scale.x = 0.02
        marker.scale.y = 0.02
        marker.scale.z = 0.02

        marker.color.r = 0.0
        marker.color.g = 0.0
        marker.color.b = 0.0
        marker.color.a = 1.0

        if _op == 0:
            marker.color.r = 1.0
        elif _op == 1:
            marker.color.g = 1.0
        else:
            marker.color.b = 1.0
            marker.color.g = 0.5
            marker.color.r = 0.5

        return marker


if __name__ == "__main__":
    rospy.init_node("detector", anonymous=False)
    pp = pcl_processor()
    rospy.spin()