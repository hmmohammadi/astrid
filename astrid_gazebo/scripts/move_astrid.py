import rospy
from geometry_msgs.msg import Pose, Twist
import time
from gazebo_msgs.msg import ModelState, ModelStates
import math


def move(velocity_publisher, speed, distance):

    model_msg = ModelState()
    
    global model 
    model_msg.model_name = 'gazebo2'
    model_msg = model
    # twist_msg = Twist()
    # pose_msg = Pose()
    
    print(model_msg)
    ### 
    # twist_msg.linear.x = abs(speed)


    # model_msg.twist = twist_msg
    # model_msg.name = 'gazebo2'
    model_msg.twist.linear.x = abs(speed)

    
    # Get current location
    global x, y

    # Save the initial locations
    x_0 = model.pose.position.x
    y_0 = model.pose.position.y
    distance_moved = 0
    loop_rate = rospy.Rate(10) # we publish the velocity at 10 Hz (10 times per second)
    while True :
        rospy.loginfo("Astrid moves ")
        # publish data to move turtle
        velocity_publisher.publish(model_msg)
        loop_rate.sleep()

        distance_moved = abs( math.sqrt(((x-x_0)**2) + (y-y_0)**2) )

        print(distance_moved)

        if  (distance_moved < distance):
            rospy.loginfo("reached !!!!")
            break

    # stop the robot        
    model_msg.twist.linear.x = 0
    velocity_publisher.publish(model_msg)



def stateCallback(state):
    global x
    global y, yaw
    global model
    pose = Pose()
    pose = state.pose[1]
    twist = Twist()
    twist = state.twist[1]
    model = ModelState()
    model.pose = pose
    model.twist = twist
    x = state.pose[1].position.x
    y = state.pose[1].position.y
    yaw = state.pose[1].orientation.z
    # print('x', x)
    # print('y', y)
    # print('z', yaw)
    # pass

if __name__=="__main__":
    # get_state()
    try:
        rospy.init_node('astrid_pose', anonymous=True)

        set_model_state_topic = "/gazebo/set_model_state"
        vel_publisher = rospy.Publisher(set_model_state_topic, ModelState, queue_size=10)

        current_position_topic = '/gazebo/model_states'
        pose_subscriber = rospy.Subscriber(current_position_topic, ModelStates, callback=stateCallback)
        time.sleep(2)
        move(vel_publisher, 1, 2)

    except rospy.ROSInterruptException:
        rospy.loginfo("node terminated.")


    # pass
