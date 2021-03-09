import rospy
from geometry_msgs.msg import Pose, Twist
import time
from gazebo_msgs.msg import ModelStates


def move():

    vel_message = ModelState()
    vel_message.model_name = "gazebo2"
    vel_message.x = 3

    # vel_publisher = 
    print(vel_message)
    pass

def get_model(model):
    # model.model_name = "gazebo2"
    # print(model.data)
    # rospy.loginfo(model.model_name['gazebo2'].pose)
    # model.name <list>
    # model.pose <list>
    # model.twist <list>
    # model.twist[0].angular.x
    # print((model.twist[0].angular.x))4
    # print('x', model.twist[1].linear.x)
    # print('y', model.twist[1].linear.y)
    # print('z', model.twist[1].angular.z)
    # data = model.pose[1].position
    t = model.twist[1]
    p = model.pose[1]
    print("robot pose")
    print(p)
    print("robot twsit")
    print(t)



def get_state():
    # alici bit node belirle
    # init_node(subscriber_node_name, is_uniqe)
    rospy.init_node('get_gazebo2', anonymous=True)
    # Subscriber(topic_name, topic massage type, callback function)
    rospy.Subscriber('/gazebo/model_states', ModelStates, callback=get_model)
    rospy.spin()


def stateCallback(state):
    pass

if __name__=="__main__":
    # # get_state()
    # try:
    #     rospy.init_node('astrid_pose', anonymous=True)

    #     set_model_state_topic = "/gazebo/set_model_state"
    #     vel_publisher = rospy.Publisher(set_model_state_topic, ModelStates, queue_size=10)

    #     current_position_topic = '/gazebo/model_states'
    #     pose_subscriber = rospy.Subscriber(current_position_topic, ModelStates, callback=stateCallback)
    #     time.sleep(2)

    # except rospy.ROSInterruptException:
    #     rospy.loginfo("node terminated.")
    get_state()


    pass
