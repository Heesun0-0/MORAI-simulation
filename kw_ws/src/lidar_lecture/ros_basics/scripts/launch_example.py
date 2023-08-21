#! /usr/bin/env python3
import rospy
from std_msgs.msg import String

rospy.init_node('launch_example')
a = rospy.get_param("/hello_world/a")
rate = rospy.Rate(10)
pub =rospy.Publisher('chatter', String, queue_size=10)


while not rospy.is_shutdown():
    str_data = a
    pub.publish(str_data)
    rate.sleep()
# 과제 foo, bar, b 에 대해서도 publish 하는 코드 만들기