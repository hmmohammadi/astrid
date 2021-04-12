#!/usr/bin/env python3
import cv2
import numpy as np
import glob
import random

import sys
import rospy
import cv2
from std_msgs.msg import String
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError


class ImageConvertor:
    def __init__(self):
        self.bridge = CvBridge()
        self.image_sub = rospy.Subscriber("/camera/image_raw", Image, self.callback)

    def callback(self, data):
        print("getting image")
        try:
            cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
        except CvBridgeError as e:
            print(e)
                # Load Yolo
        net = cv2.dnn.readNet("/home/muvahhidkilic/Desktop/yolov3_final.weights", "/home/muvahhidkilic/Desktop/yolov3.cfg")

        # Name custom object
        classes = ['20-km','30-km','dur','giris-yok','ileri-saga','ileri-sola','ileriden-saga','ileriden-sola','isik-kirmizi','isik-sari','isik-yesil','tasita-kapali','yasak-sag','yasak-sol','durak','yasak-park','park','20-km-sonu']

        # Images path
        # images_path = glob.glob(r"/home/ensar/Desktop/darknet/data/images/ileri_sag-635.jpg")

        layer_names = net.getLayerNames()
        output_layers = [layer_names[i[0] - 1] for i in net.getUnconnectedOutLayers()]
        colors = np.random.uniform(0, 255, size=(len(classes), 3))


        # Loading image
        img = cv_image
        img = cv2.resize(img, None, fx=0.4, fy=0.4)
        height, width, channels = img.shape

        # Detecting objects
        blob = cv2.dnn.blobFromImage(img, 0.00392, (416, 416), (0, 0, 0), True, crop=False)

        net.setInput(blob)
        outs = net.forward(output_layers)

        # Showing informations on the screen
        class_ids = []
        confidences = []
        boxes = []
        for out in outs:
            for detection in out:
                scores = detection[5:]
                class_id = np.argmax(scores)
                confidence = scores[class_id]
                if confidence > 0.3:
                    # Object detected
                    print(class_id)
                    center_x = int(detection[0] * width)
                    center_y = int(detection[1] * height)
                    w = int(detection[2] * width)
                    h = int(detection[3] * height)

                    # Rectangle coordinates
                    x = int(center_x - w / 2)
                    y = int(center_y - h / 2)

                    boxes.append([x, y, w, h])
                    confidences.append(float(confidence))
                    class_ids.append(class_id)

        indexes = cv2.dnn.NMSBoxes(boxes, confidences, 0.5, 0.4)
        print(indexes)
        font = cv2.FONT_HERSHEY_PLAIN
        for i in range(len(boxes)):
            if i in indexes:
                x, y, w, h = boxes[i]
                label = str(classes[class_ids[i]])
                color = colors[class_ids[i]]
                cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
                cv2.putText(img, label , (x-60, y +30), font, 2, color, 2)


        cv2.imshow("Image", img)
        key = cv2.waitKey(1)


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
