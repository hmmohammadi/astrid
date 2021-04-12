import rospy
import cv2
from sensor_msgs.msg  import LaserScan
import math
from astrid_control.msg import Way_Point, OnePoint
import numpy as np

way_point = Way_Point()
def scan_callback(data):
    global way_point
    rad = 0.0174532925
    ranges = np.asarray(data.ranges)
    for a in range(len(ranges)):
        if math.isinf(ranges[a]):
            ranges[a] = 30
    # print(ranges)
    #once sol ve sagda 15 30 45 60 derecelik acilarin orta noktalarini aliyoruz
    right15 = [(math.sin(15*rad)*ranges[15]),(math.cos(15*rad)*ranges[15])]
    right30 = [(math.sin(30*rad)*ranges[30]),(math.cos(30*rad)*ranges[30])]
    right45 = [(math.sin(45*rad)*ranges[45]),(math.cos(45*rad)*ranges[45])]
    right60 = [(math.sin(60*rad)*ranges[60]),(math.cos(60*rad)*ranges[60])]
    left15 = [(math.sin(165*rad)*ranges[165]),(math.cos(165*rad)*ranges[165])]
    left30 = [(math.sin(150*rad)*ranges[150]),(math.cos(150*rad)*ranges[150])]
    left45 = [(math.sin(135*rad)*ranges[135]),(math.cos(135*rad)*ranges[135])]
    left60 = [(math.sin(120*rad)*ranges[120]),(math.cos(120*rad)*ranges[120])]


    first_wp = (np.add(right15,left15))/2
    second_wp = (np.add(right30,left30)) /2
    third_wp = (np.add(right45,left45))/2
    fourth_wp = (np.add(right60,left60))/2

    way_point.first_waypoint.x = first_wp[0]
    way_point.first_waypoint.y = first_wp[1]
    way_point.second_waypoint.x = second_wp[0]
    way_point.second_waypoint.y = second_wp[1]
    way_point.third_waypoint.x = third_wp[0]
    way_point.third_waypoint.y = third_wp[1]
    way_point.fourth_waypoint.x = fourth_wp[0]
    way_point.fourth_waypoint.y = fourth_wp[1]

    # temp = 0
    # for a in range(len(ranges)):
    #     if ranges[a] > temp and ranges[a]<21:
    #         temp = ranges[a]
    #         uzak = [(math.sin(a*rad)*ranges[a]),(math.cos(a*rad)*ranges[a])]
    #         way_point.fourth_waypoint.y = uzak[0]
    #         way_point.fourth_waypoint.x = -1*uzak[1]


        # return way_point
    print('WAYPOINT: \n',way_point)





def scan_resutls():
    global way_point

    rospy.init_node('scan_node', anonymous = False)

    pub = rospy.Publisher("/scan_publisher",Way_Point,queue_size=10)
    # #rospy.init_node('average_publisher', anonymous=True)
    rospy.Subscriber("/scan", LaserScan, scan_callback)
    rate = rospy.Rate(1)

    while not rospy.is_shutdown():
        pub.publish(way_point)
        rate.sleep()
    #node bitene kadar kok dönüyor.


    #print(rangePublish)
    #text = rangePublish
    #print(text)




if __name__=="__main__":
    scan_resutls()
    rospy.spin()
