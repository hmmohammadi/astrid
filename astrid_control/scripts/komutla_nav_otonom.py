import cv2
import rospy
from astrid_control.msg import Way_Point, OnePoint
from nav_msgs.msg import Odometry
import move_base
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib

global odometri
global waynokta
odometri = Odometry()
waynokta = Way_Point()

def movebase_client(waypoint_veri,odom_veri):

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()
   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
   # Move 0.5 meters forward along the x axis of the "map" coordinate frame

    goal.target_pose.pose.position.x = waypoint_veri.fourth_waypoint.x + odom_veri.pose.pose.position.x
    goal.target_pose.pose.position.y = waypoint_veri.fourth_waypoint.y + odom_veri.pose.pose.position.y

    goal.target_pose.pose.orientation.w = 1.0
    print(goal.target_pose.pose)
    client.send_goal(goal)

   # Sends the goal to the action server.

   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result()




def scan_subs_callback(data):
    global odometri
    global waynokta
    waynokta = data

    #movebase_client(waynokta,odometri)

def odom_subs_callback(data):
    global odometri
    global waynokta
    odometri = data
    print(movebase_client(waynokta,odometri))

def getRanges():
   rospy.init_node('scannerr',anonymous=False)
   rospy.Subscriber('/scan_publisher',Way_Point,scan_subs_callback)
   rospy.Subscriber('/odom', Odometry, odom_subs_callback)

if __name__=="__main__":
    getRanges()
    rospy.spin()
