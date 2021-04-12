#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Pose, Twist, Transform, TransformStamped
from gazebo_msgs.msg import LinkStates
from std_msgs.msg import Header
import numpy as np
import math
import tf2_ros

class OdometryNode:
    # set publishers
    pub_odom = rospy.Publisher('/odom', Odometry, queue_size=1)

    def __init__(self):
        # init internals
        self.l_rec_pose = Pose()
        self.l_rec_twist = Twist()
        self.l_rec_stamp = None

        # set the update rate 0.02 50
        rospy.Timer(rospy.Duration(.02), self.timer_callback) # 20hz
        
        self.tf_pub = tf2_ros.TransformBroadcaster()

        #
        rospy.Subscriber('/gazebo/link_states', LinkStates, self.sub_robot_pose_update)

    def sub_robot_pose_update(self,msg):
        # Find the index of the astrid
        try:
            arr_index = msg.name.index('astrid::base_link')
        except ValueError as e:
            # Wait for Gazebo to startup
            pass
        else:
            # Extract our current position information
            self.l_rec_pose = msg.pose[arr_index]
            self.l_rec_twist = msg.twist[arr_index]
        self.l_rec_stamp = rospy.Time.now()
    
    def timer_callback(self, event):
        if self.l_rec_stamp is None:
            return
        cmd = Odometry()
        cmd.header.stamp = self.l_rec_stamp
        cmd.header.frame_id = 'odom'
        cmd.child_frame_id = 'base_link'
        cmd.pose.pose = self.l_rec_pose
        cmd.twist.twist = self.l_rec_twist
        self.pub_odom.publish(cmd)

        tf = TransformStamped(
            header=Header(
                frame_id = cmd.header.frame_id,
                stamp=cmd.header.stamp   
            ),
            child_frame_id=cmd.child_frame_id,
            transform=Transform(
                translation=cmd.pose.pose.position,
                rotation=cmd.pose.pose.orientation
            )
        )
        self.tf_pub.sendTransform(tf)
        
# Start the node
if __name__ == '__main__':
    rospy.init_node("gazebo_odometry_node")
    node = OdometryNode()
    rospy.spin()

