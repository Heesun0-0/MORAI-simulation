#!/usr/bin/env python3
import rospy
import math
from sensor_msgs.msg import PointCloud, ChannelFloat32
from geometry_msgs.msg import Point32
def generate_sphere_cloud():
    cloud_msg = PointCloud()
    cloud_msg.header.frame_id = "sphere"
    # cloud_msg.header.stamp = rospy.Time.now()
    for i in range(0, 628, 10):
        theta = 2 * 3.14 - i * 0.01
        _z = math.sin(theta)
        for j in range(0, 628, 10):
            phi = 2 * 3.14 - j * 0.01
            _x = math.cos(theta) * math.cos(phi)
            _y = math.cos(theta) * math.sin(phi)
            _p =Point32()
            _p.x = _x
            _p.y = _y
            _p.z = _z
            cloud_msg.points.append(_p)
    return cloud_msg
def main():
    rospy.init_node("sphere_cloud_publisher")
    pub = rospy.Publisher("sphere_cloud", PointCloud, queue_size=10)
    rate = rospy.Rate(1)
    while not rospy.is_shutdown():
        cloud_msg = generate_sphere_cloud()
        pub.publish(cloud_msg)
        rate.sleep()
if __name__ == "__main__":
    try:
        main()
    except rospy.ROSInterruptException:
        pass