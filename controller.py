#!/usr/bin/env python3

import rospy
from nav_msgs.msg import Odometry
from tf.transformations import euler_from_quaternion
from geometry_msgs.msg import Point, Twist
from math import atan2, sqrt, pi

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

POINTS = (Point(x = 0, y = 0),Point(x = 2, y = 0),Point(x = 2, y = 2))
ROTATE_SPEED = 0.7
LINEAR_SPEED = 0.40
""" goal = Point()	#set goal point
goal.x = 5
goal.y = 5 """
state = 0
step = 0

while not rospy.is_shutdown():
	""" goal = POINTS[state]
	inc_x = goal.x - x	#get position difference between current and goal
	inc_y = goal.y - y """

	if state == 0:
		if step < 8:
			speed.linear.x = LINEAR_SPEED	
			speed.angular.z = 0
		else:
			step = 0
			state +=1
	elif state == 1:
		if step < 6:
			speed.linear.x = 0	
			speed.angular.z = 0
		else:
			step = 0
			state +=1
	elif state == 2:
		if step < 15:
			speed.linear.x = 0	
			speed.angular.z = -ROTATE_SPEED
		else:
			step = 0
			state +=1
	elif state == 3:
		if step < 6:
			speed.linear.x = 0	
			speed.angular.z = 0
		else:
			step = 0
			state +=1
	elif state == 4:
		if step < 8:
			speed.linear.x = LINEAR_SPEED	
			speed.angular.z = 0
		else:
			speed.linear.x = 0
			step = 0
			state +=1
	elif state == 5:
		pub.publish(speed)
		raise KeyboardInterrupt		
	
	

	step += 1
	""" # speed.angular.z: +ve means CLOCKWISE, -ve means ANTICLOCK
	angle_to_goal = atan2(inc_y, inc_x)	#get angle between current and goal
	#if angle_to_goal > pi: angle_to_goal = pi - angle_to_goal 
	distance_to_goal = sqrt(inc_x**2 + inc_y**2)
	angle_diff = angle_to_goal - theta
	if angle_diff > pi: angle_diff -= pi
	if angle_diff < -pi: angle_diff += pi

	rotate_speed = ROTATE_SPEED[0] if abs(angle_diff) > 0.5 else ROTATE_SPEED[1]
	if angle_diff > 0.15:	#if angle is not small enough
		speed.linear.x = 0.0	
		speed.angular.z = -rotate_speed
	elif angle_diff < -0.15:
		speed.linear.x = 0.0	
		speed.angular.z = rotate_speed
	elif distance_to_goal < 0.1:
		if state != 2:
			state += 1
		print(f'point: {state}')
	else:
		speed.linear.x = LINEAR_SPEED if state != 2 else 0	#go straight
		speed.angular.z = 0.0
	
	step_count += 1 """

	print(f'x: {x:.3f}, y: {y:.3f}, theta: {theta:.3f}, ')
	#print(f'inc_x: {inc_x:.3f}, inc_y: {inc_y:.3f}')
	#print(f'angle_to_goal: {angle_to_goal:.3f}, distance_to_goal: {distance_to_goal:.3f}, angle_diff: {angle_diff:.3f}')
	print(f'speed.linear.x: {speed.linear.x}, speed.angular.z: {speed.angular.z}')
	print(f'step_count: {step}, state: {state}')


	pub.publish(speed)	#send current speed to ROS
	r.sleep()
