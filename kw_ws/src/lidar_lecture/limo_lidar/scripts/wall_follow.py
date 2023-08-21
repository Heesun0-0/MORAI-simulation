import rospy
from sensor_msgs.msg import LaserScan
from geometry_msgs.msg import Twist
import math
import numpy as np

class WallFollowing:
    def __init__(self):
        rospy.init_node('wall_following')
        self.cmd_pub = rospy.Publisher('/cmd_vel', Twist, queue_size=10)
        self.scan_sub = rospy.Subscriber('/limo/scan', LaserScan, self.laser_callback)
        self.a = 0
        self.b = 0
        self.error_i = 0

    def publish_cmd(self):
        cmd = Twist()
        cmd.linear.x = 0.3
        cmd.angular.z = 0
        control = self.slope_p() + self.distance_i()

        if control > 1:
            cmd.linear.x = 0.1
            cmd.angular.z = 0.6
        elif control < -1.0:
            cmd.linear.x = 0.1
            cmd.angular.z = -0.6
        else:
            cmd.linear.x = 0.3 - control * 0.24
            cmd.angular.z = control * 0.6
        
        self.cmd_pub.publish(cmd)

    def laser_callback(self, scan):
        x_vec, y_vec = [], []

        for i in range(len(scan.ranges)):
            if not math.isinf(scan.ranges[i]):
                angle_temp = scan.angle_min + i * scan.angle_increment
                x_temp = scan.ranges[i] * math.cos(angle_temp)
                y_temp = scan.ranges[i] * math.sin(angle_temp)

                if y_temp > 0 and -0.3 < x_temp < 0.3:
                    x_vec.append(x_temp)
                    y_vec.append(y_temp)

        x = np.array(x_vec)
        y = np.array(y_vec)

        A = np.vstack([x, np.ones(len(x))]).T
        answer = np.linalg.lstsq(A, y, rcond=None)[0]
        self.a = answer[0]
        self.b = answer[1]
        rospy.loginfo(f"inclination : {self.a}, y-intercept : {self.b}")

    def slope_p(self):
        Kp = 5
        object_slope = 0
        error = self.a

        if abs(self.a) < 0.01:
            self.a = 0

        P_control = Kp * error
        return P_control

    def distance_i(self):
        Ki = 0.1
        object_distance = 1
        error = -(object_distance - self.b)
        self.error_i += error

        if self.error_i > 10:
            self.error_i = 10
        elif self.error_i < -10:
            self.error_i = -10
        
        I_control = Ki * self.error_i
        return I_control

if __name__ == '__main__':
    wf = WallFollowing()
    rate = rospy.Rate(10)

    while not rospy.is_shutdown():
        wf.publish_cmd()
        rate.sleep()
