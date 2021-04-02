#! /usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Twist, Transform, TransformStamped
from gazebo_msgs.msg import LinkStates
from std_msgs.msg import Header
import numpy as np
import math
import tf2_ros
import time

## hata aliyorum bi bekler misin__tamam hata nerede sence__tamam bi bakıyorum kodu kopyala da bakabilirsin 

pose  = Pose()
twist = Twist()
tf_pub = tf2_ros.TransformBroadcaster()

def publish_odom(odom_pub):

    # init internals
    global pose 
    global twist
    global tf_pub
    # global pub_odom

    # pub_odom = rospy.Publisher('/odom', Odometry, queue_size=1) #silelim bunu???
    loop_rate = rospy.Rate(50)#ÇOK biliyoum :) __ee noldu
    odom = Odometry()
    while not rospy.is_shutdown():
        odom.header.frame_id = 'odom'
        odom.child_frame_id = 'base_link'
        odom.pose.pose = pose
        odom.twist.twist = twist 
        odom.header.stamp = rospy.Time.now()

        tf = TransformStamped(
            header=Header(
                frame_id = odom.header.frame_id,
                stamp=odom.header.stamp   
            ),
            child_frame_id=odom.child_frame_id,
            transform=Transform(
                translation=odom.pose.pose.position,
                rotation=odom.pose.pose.orientation
            )
        )
        odom_pub.publish(odom) # odometri değerleri odom topic ile pub edildi kucuk buyuk harf
        tf_pub.sendTransform(tf) #aynı şekilde tf de
        loop_rate.sleep()

        



    







def robot_pose_update(data): #gazebodan tf değerleri alındı (topic üzerinden)
    global pose
    global twist
    
    try:
        arr_index = data.name.index('astrid::base_link') 
    except ValueError as e:
        # Wait for Gazebo to startup
        pass
    else: # BU NE ABİ İF İ NERDE ifi try execpt bende ilk defa goruyorum
        # arr_index = data.name.index('astrid::base_link')
        pose =  data.pose[arr_index]
        twist = data.twist[arr_index]

    
    # print("pose", pose)
    # print("\ntwist", twist)



def sub(): #node oluşturuldu ve topic dinleniyor
    # rospy.init_node('listener', anonymous=True)
    rospy.Subscriber('/gazebo/link_states', LinkStates, robot_pose_update)
    # rospy.spin()


if __name__=="__main__":

    rospy.init_node("astrid_odometry_node", anonymous=True)

    odom_pub = rospy.Publisher('/odom', Odometry, queue_size=10)
    tf_pose_sub = rospy.Subscriber('/gazebo/link_states', LinkStates, robot_pose_update)
    # sub()
    time.sleep(2)
    publish_odom(odom_pub)
    



