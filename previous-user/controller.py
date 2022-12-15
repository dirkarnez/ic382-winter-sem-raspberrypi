#!/usr/bin/env python3

import time
import numpy
import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2

x = 0.0
y = 0.0 
theta = 0.0

def newOdom(msg):
    global x
    global y
    global theta

    x = msg.pose.pose.position.x
    y = msg.pose.pose.position.y

    rot_q = msg.pose.pose.orientation
    (roll, pitch, theta) = euler_from_quaternion([rot_q.x, rot_q.y, rot_q.z, rot_q.w])

rospy.init_node("speed_controller")

sub = rospy.Subscriber("/odom", Odometry, newOdom)
pub = rospy.Publisher("/cmd_vel", Twist, queue_size = 1)

speed = Twist()

r = rospy.Rate(4)



goal = Point()
goal.x = 2.5
goal.y = 0

flag = 1
error_y = 0

while not rospy.is_shutdown():
	
	inc_x = goal.x -x
	#if flag == 0:
	inc_y = goal.y - y
	#else:
	#inc_y = goal.y - y  + error_y
	print("inc_x=",inc_x)
	print("inc_y=",inc_y)
	print("x = ",x,", y = ",y,", theta = ", theta)
	'''if abs(inc_y) < 0.1 and abs(inc_x) < 0.1 and (flag == 0):
		t = Twist()
		pub.publish(t)
		goal.x = 0.00488
		goal.y = 0.00488
		error_y = y
		flag = 1'''

	if (flag == 2):
		goal.x = 2.5
		goal.y = -2.5

	if (flag == 3):
		goal.x = 6
		goal.y = -2.5
	
	
	
	

	#First move forward

	if(flag==1):
		if (abs(inc_x)<0.2):
			speed.linear.x = 0.0
			speed.angular.z = 0.0
			flag = 2
			print("enter stage 2")
			pub.publish(speed)
			time.sleep(5)
			first_value_store = abs(theta)
			goal_value_store = first_value_store + ( numpy.pi / 4.6)
			if(goal_value_store > numpy.pi):
				goal_value_store = goal_value_store - numpy.pi
		else:
			speed.linear.x = 0.5
			speed.angular.z = 0.0
			print("stage 1 running")
		
	
	#Second turn right 90 degrees
	elif(flag==2):
		#angle_to_goal = atan2(inc_y, inc_x)
		#if(goal_value_store > abs(theta)):
		#if abs(angle_to_goal + theta) > 0.3:

		if(abs(abs(theta) - goal_value_store)>0.3):
			speed.linear.x = 0.0
			speed.angular.z = -0.8
			print("theta", theta)
			print("abc", abs(theta) - goal_value_store)
			print("stage 2 running")
		else:
			speed.linear.x = 0.0
			speed.angular.z = 0.0
			flag = 3
			print("enter stage 3")
			pub.publish(speed)
			time.sleep(5)

	#Third move forward
	elif(flag==3):
		if(abs(inc_x)<0.3):
			speed.linear.x = 0.0
			speed.angular.z = 0.0
			print("stage 3 complete")
			flag = 4
		else:
			speed.linear.x = 0.5
			speed.angular.z = 0.0
			print("stage 3 running")
	#Complete
	elif(flag==4):
		print("stage 4 complete")
	
	

	pub.publish(speed)
	r.sleep()
		








