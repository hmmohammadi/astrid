#!/usr/bin/env python3
import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

class ImageConvertor:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/astrid/camera/image_raw", Image, self.callback)
    
    def callback(self, data):
        print("getting image")
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
        
        (rows, cols, channels) = cv_image.shape
        if cols > 200 and rows > 200 :
            cv2.circle(cv_image, (100, 100), 90, 255)
        
        cv2.imshow("Image", cv_image)
        cv2.waitKey(3)

def main(args):
    ic = ImageConvertor()
    rospy.init_node("image_convertor", anonymous=True)
    try:
        rospy.spin()
    except KeyboardInterrupt:
        print("Shutting down ...!!!")
    
    cv2.destroyAllWindows()


if __name__=="__main__":
    main(sys.argv)

