#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2, sqrt
from datetime import datetime

x = 0.0 	#current position x
y = 0.0 	#current position y
theta = 0.0	#current facing angle

def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x	#get current position
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation	#get current facing angle
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("speed_controller")	#init

sub = rospy.Subscriber("/odom", Odometry, newOdom)	#to get data from ROS/ordmoetry
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)	#to send data to ROS

speed = Twist()

r = rospy.Rate(4)

goal_array = [Point(x = 0, y = 0),Point(x = 5, y = 0),Point(x = 5, y = 5),Point(x = 0, y = 5)]
goal = Point()	#set goal point
goal.x = 5
goal.y = 5
state = 0

step_count = 0

while not rospy.is_shutdown():
    goal = goal_array[state]

    

    inc_x = goal.x - x	#get position difference between current and goal
    inc_y = goal.y - y

    angle_to_goal = atan2(inc_y, inc_x)	#get angle between current and goal
    distance_to_goal = sqrt(inc_x**2 + inc_y**2)
    speed.linear.x = 0.5
    """ if angle_to_goal - theta > 0.1:	#if angle is not small enough
        speed.linear.x = 0.0	
        speed.angular.z = 0.3
    elif angle_to_goal - theta < 0.1:
        speed.linear.x = 0.0	
        speed.angular.z = -0.3
    elif distance_to_goal < 0.1:
        if state != 3:
            state += 1
        else:
            state = 0
        print(f'state: {state}')
    else:
        speed.linear.x = 0.5	#go straight
        speed.angular.z = 0.0 """
    print(datetime.now())
    print(f'x: {x}, y:{y}')
    print(f'inc_x: {inc_x}, inc_y: {inc_y}')
    print(f'angle: {angle_to_goal}, distance: {distance_to_goal}')
    print(f'linear speed: {speed.linear.x}, angular speed: {speed.angular.z}')
    print(f'step_count: {step_count}')
    step_count += 1



    pub.publish(speed)	#send current speed to ROS
    r.sleep()
