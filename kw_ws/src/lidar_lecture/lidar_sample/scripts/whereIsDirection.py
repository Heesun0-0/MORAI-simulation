#! /usr/bin/python3

import rospy
import math
from sensor_msgs.msg import LaserScan

import numpy as np
import random


class pcl_processor:
    __slots__ = ['sub_laser']
    def __init__(self):
        self.sub_laser = rospy.Subscriber(
            "/scan",
            LaserScan,
            callback=self.judge
        )

    def showOutput(self, _nlist:list) -> None:
        print("---------------------------\n")
        _text = ""
        if _nlist[0] > 5:
            _text += f"right obstacle : {_nlist[0]}\n"
        if _nlist[1] > 5:
            _text += f"front obstacle : {_nlist[1]}\n"
        if _nlist[2] > 5:
            _text += f"left obstacle : {_nlist[2]}\n"
        print(_text)
        print("---------------------------\n")

    def judge(self, _ls:LaserScan):
        _right = (-2.35619, -0.7895398)
        _front = (-0.7895398, 0.7895398)
        _left = (0.7895398, 2.35619)

        rightNum = 0
        frontNum = 0
        leftNum = 0

        _rMin = _ls.angle_min
        _rInc = _ls.angle_increment
        numOfPoint = len(_ls.ranges)

        eStopPoint = 0.5

        currentRadian = _rMin

        for i in range(0, numOfPoint):
            if _ls.ranges[i] < eStopPoint:
                if currentRadian >= _right[0] and currentRadian < _right[1]:
                    rightNum += 1
                elif currentRadian >= _front[0] and currentRadian < _front[1]:
                    frontNum += 1
                elif currentRadian >= _left[0] and currentRadian < _left[1]:
                    leftNum += 1
            currentRadian += _rInc

        self.showOutput([rightNum, frontNum, leftNum])


if __name__ == "__main__":
    rospy.init_node("detector", anonymous=False)
    pp = pcl_processor()
    rospy.spin()
