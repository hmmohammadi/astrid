import rospy
from geometry_msgs.msg import Pose, Twist, Point
import time
from gazebo_msgs.msg import ModelState, ModelStates
import math

# global model, x, y
x = 0
y = 0

def move(vel_publisher, speed, dis ):

    ##
    # global model
    model_msg = ModelState()
    # model_msg.pose = model.pose
    # model_msg.twist = model.twist
    model_msg.model_name = 'astrid'
    ###
    # print('model_msg', model_msg)
    ####

    model_msg.twist.linear.x = speed
    #print(model_msg)
    distance_moved = 0
    loop_rate = rospy.Rate(5) # we publish the velocity at 10 Hz (10 times per second)
    ##
    global x, y
    x_0 = x
    y_0 = y

    while True :
        # rospy.loginfo("Astrid moves ")
        # publish data to move turtle
        vel_publisher.publish(model_msg)
        loop_rate.sleep()

        distance_moved = abs( math.sqrt(((x-x_0)**2) + (y-y_0)**2) )

        print(distance_moved+0.4)

        if not (distance_moved+0.4 < dis):
            rospy.loginfo("reached !!!!")
            # while True:
            #     pass
            break

    # stop the robot        
    model_msg.twist.linear.x = 0
    # vel_publisher.publish(model_msg)




def stateCallback(data):
    ## global 
    # global model
    # model = ModelState()
    # model.pose = data.pose[1]
    # model.twist = data.twist[1]
    #print(data)
    global x, y
    x = data.pose[1].position.x
    y = data.pose[1].position.y

if __name__=="__main__":
    try:
        rospy.init_node('astrid_pose', anonymous=True)

        set_model_state_topic = "/gazebo/set_model_state"
        vel_publisher = rospy.Publisher(set_model_state_topic, ModelState, queue_size=10)

        current_position_topic = '/gazebo/model_states'
        pose_subscriber = rospy.Subscriber(current_position_topic, ModelStates, callback=stateCallback)
        time.sleep(2)
        move(vel_publisher, 10, 6)

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")