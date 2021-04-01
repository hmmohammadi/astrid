import rospy

from ackermann_msgs.msg import AckermannDrive
from geometry_msgs.msg import Twist

class teleopAstrid:
    def __init__(self):
        rospy.init_node("ackermann_controller", anonymous=False)
        self.astrid = AckermannDrive()
        self.vel_publisher = rospy.Publisher(cmd_vel_topic, AckermannDrive, queue_size=1)
        # self.sub_topic = "/ackermann_controller"
        # self.vel_subscriber = rospy.Subscriber(self.sub_topic, Twist, )
    
    def forward(self):
        self.astrid.speed = 2
        self.astrid.steering_angle = 0
        self.astrid.steering_angle_velocity = 0
    

    def move(self):
        self.loop_rate = rospy.Rate(8)
        while not rospy.is_shutdown():
            self.forward()
            self.vel_publisher.publish(self.astrid)
            self.loop_rate.sleep()
            # break
            break
    



if __name__=="__main__":
    astrid = teleopAstrid()
    astrid.move()