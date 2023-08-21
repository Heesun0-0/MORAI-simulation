#! /usr/bin/env python3
  
import rospy
from sensor_msgs.msg import CompressedImage, Image
from cv_bridge import CvBridge
import cv2
import numpy as np

class Lkas:
    def __init__(self):
        rospy.init_node('bird_eye_view', anonymous=True)
        self.bridge=CvBridge()
        self.pub= rospy.Publisher('/modified_compressed_img',Image, queue_size=10)
        self.sub = rospy.Subscriber('/image_jpeg/compressed', CompressedImage, self.imgCB)
        rospy.spin()
    
    def detect_color(self, img):
        # Convert to HSV color space
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

        # Define range of white color in HSV
        white_lower = np.array([0, 0, 150])
        white_upper = np.array([255, 10, 255])

        # Threshold the HSV image to get only white colors
        white_mask = cv2.inRange(hsv, white_lower, white_upper)
        cv2.imshow("white_mask", white_mask)
        white_color = cv2.bitwise_and(img, img, mask=white_mask)
        cv2.imshow("white_color", white_color)
        return white_color

    def img_wrap(self, img):
        self.img_x, self.img_y = img.shape[1], img.shape[0]
        src_center_offset = [200, 315]
        src = np.float32(
            [
                [0, 479],
                [src_center_offset[0], src_center_offset[1]],
                [640 - src_center_offset[0], src_center_offset[1]],
                [639, 479],
            ]
        )
        cv2.circle(img, (0, 479), 10, 255,10)
        cv2.circle(img, (src_center_offset[0], src_center_offset[1]), 10, 255,10)
        cv2.circle(img, (640 - src_center_offset[0], src_center_offset[1]), 10, 255,10)
        cv2.circle(img, (639,479), 10, 255,10)

        dst_offset = [round(self.img_x *0.125),0]

        dst = np.float32(
            [
                [dst_offset[0], self.img_y],
                [dst_offset[0], 0],
                [self.img_x - dst_offset[0],0],
                [self.img_x - dst_offset[0], self.img_y]

            ]
        )

        cv2.circle(img, (dst_offset[0], self.img_y), 10, (0,0,255), 10)
        cv2.circle(img, (dst_offset[0], 0), 10, (0,0,255), 10)
        cv2.circle(img, (self.img_x - dst_offset[0], 0), 10, (0,0,255), 10)
        cv2.circle(img, (self.img_x - dst_offset[0], self.img_y), 10, (0,0,255), 10)

        matrix = cv2.getPerspectiveTransform(src, dst)
        warp_img = cv2.warpPerspective(img, matrix, (self.img_x, self.img_y))

        return img, warp_img
    
    def imgCB(self, data):
        img =self.bridge.compressed_imgmsg_to_cv2(data)

        modi_img, warp_img =self.img_wrap(img)

        warp_img_msg = self.bridge.cv2_to_imgmsg(warp_img, 'bgr8')

        self.pub.publish(warp_img_msg)

        cv2.imshow("Image window",modi_img)
        cv2.imshow("warp window",warp_img)
        cv2.waitKey(1)

def main():
    rospy.init_node('lkas_node', anonymous=True)
    lk = Lkas()
    rospy.spin()

if __name__=="__main__":
    main()