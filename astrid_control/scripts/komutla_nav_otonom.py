import cv2
import rospy
from astrid_control.msg import Way_Point, OnePoint
from nav_msgs.msg import Odometry
import move_base
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
import actionlib
import math

def movebase_client(x,y,z):

   # Create an action client called "move_base" with action definition file "MoveBaseAction"
    client = actionlib.SimpleActionClient('move_base',MoveBaseAction)

   # Waits until the action server has started up and started listening for goals.
    client.wait_for_server()
   # Creates a new goal with the MoveBaseGoal constructor
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()
   # Move 0.5 meters forward along the x axis of the "map" coordinate frame



    goal.target_pose.pose.position.x = x
    goal.target_pose.pose.position.y = y

    goal.target_pose.pose.orientation.z = z
    goal.target_pose.pose.orientation.w = math.sqrt(1-z**2)

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




# def scan_subs_callback(data):
#     global odometri
#     global waynokta
#     waynokta = data
#
#     #movebase_client(waynokta,odometri)
#
# def odom_subs_callback(data):
#     global odometri
#     global waynokta
#     odometri = data
#     print(movebase_client(odometri))

def getRanges():
    poses = [[10,0],[26,0],[62,0],[77,-1],[118, 21],[80,38],[71,85],  [63,91],[41,91],  [19,45],[11,38],[-9,23],[-15,22]]
    orients = [[0,1],[0,1],[0,1], [0,1],  [0.7,0.7],[1,0],  [0.7,0.7],[1,0],  [1,0], [0.7,-0.7],  [1,0], [1,0],  [1,0]]
    rospy.init_node('scannerr',anonymous=False)
    for x in range(len(poses)):
       movebase_client(poses[x][0],poses[x][1],orients[x][0])
       if x == 4 or x == 8:
           temp = 0
           while not temp==10:
               rospy.sleep(3);
               print("duruyor")
               temp +=1

       rospy.sleep(0.3)
    print("bittiiiiiiiiiiiiiiiii-----------------")
   # rospy.Subscriber('/scan_publisher',Way_Point,scan_subs_callback)
   # rospy.Subscriber('/odom', Odometry, odom_subs_callback)

if __name__=="__main__":
    getRanges()
    rospy.spin()
