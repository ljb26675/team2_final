#!/usr/bin/env python

""" move_base_square.py - Version 1.1 2013-12-20
    Command a robot to move in a square using move_base actions..
    Created for the Pi Robot Project: http://www.pirobot.org
    Copyright (c) 2012 Patrick Goebel.  All rights reserved.
    This program is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.5
    
    This program is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details at:
    
    http://www.gnu.org/licenses/gpl.htmlPoint
      
"""

import rospy
import actionlib
from actionlib_msgs.msg import *
from geometry_msgs.msg import Pose, Point, Quaternion, Twist
from team2_final.msg import results
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from tf.transformations import quaternion_from_euler
from visualization_msgs.msg import Marker
from math import radians, pi
from projectserver.srv import *

class MoveBaseAround():
    def __init__(self):
        rospy.init_node('nav_test', anonymous=False)
        
        rospy.on_shutdown(self.shutdown)
        
        # Create a list to hold the target quaternions (orientations)
        quaternions = list()
        
        # First define the waypoints orientations as Euler angles
        euler_angles = (pi, pi/2, 0, 0, 3*pi/2)
        
        # Then convert the angles to quaternions
        for angle in euler_angles:
            q_angle = quaternion_from_euler(0, 0, angle, axes='sxyz')
            q = Quaternion(*q_angle)
            quaternions.append(q)
        
        # Create a list to hold the offset values for each waypoint
        waypoint_offset_x = (2, 0, -2, -2, 0)
        waypoint_offset_y = (0, -2, 0, 0, 2)

        # Create a list to hold the waypoints
        waypoints = list()
        
        # Publisher to manually control the robot (e.g. to stop it, queue_size=5)
        self.cmd_vel_pub = rospy.Publisher('cmd_vel', Twist, queue_size=5)
        
        # Subscribe to the move_base action server
        self.move_base = actionlib.SimpleActionClient("move_base", MoveBaseAction)
        
        rospy.loginfo("Waiting for move_base action server...")
        
        # Wait 60 seconds for the action server to become available
        self.move_base.wait_for_server(rospy.Duration(60))
        
        rospy.loginfo("Connected to move base server")
        rospy.loginfo("Starting navigation test")
        
        # Initialize a counter to track waypoints
        i = 0
        firstwp = True
	symboldetected = False
	symbolcolor = 0
	symbolpositionx = 0
	symbolpositiony = 0

 	result = Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)
	print(result)

	while i < 5 and not rospy.is_shutdown():
            while result.success == False:
                # Ask server to get waypoint 
 	        result = Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)
	    #generate the waypoint
            waypoints.append(Pose(Point(result.waypointx + waypoint_offset_x[i], result.waypointy + waypoint_offset_y[i], 0.0), quaternions[i]))

   	    # Intialize the waypoint goal
            goal = MoveBaseGoal()
          
            # Use the map frame to define goal poses
            goal.target_pose.header.frame_id = 'map'
           
            # Set the time stamp to "now"
            goal.target_pose.header.stamp = rospy.Time.now()
           
            # Set the goal pose to the i-th waypoint
            goal.target_pose.pose = waypoints[i]
            
            # Start the robot moving toward the goal
            self.move(goal)
	    
    	    self.img_analysis = rospy.Subscriber("/analysis",results,self.callback_analysis)
	    print (self.img_analysis)

	    while self.img_analysis.symboldetected == False:
 	        #call image analysis topic
 	        #image_analysis()
                self.img_analysis = rospy.Subscriber("/analysis",results,self.callback_analysis)

	    firstwp = False
	    symboldetected = self.img_analysis.symboldetected
      	    symbolcolor = self.img_analysis.symbolcolor
	    symbolpositionx = self.result.waypointx
	    symbolpositiony = self.result.waypointy
    	    
  	    i +=1
        
    def callback_analysis(self,data):
        try:
            #read image analysis topic
            img_result = data.data
	    return img_result
    	except rospy.ServiceException, e:
      	    print(e)

    def move(self, goal):
            # Send the goal pose to the MoveBaseAction server
            self.move_base.send_goal(goal)
            
            # Allow 1 minute to get there
            finished_within_time = self.move_base.wait_for_result(rospy.Duration(60)) 
            
            # If we don't get there in time, abort the goal
            if not finished_within_time:
                self.move_base.cancel_goal()
                rospy.loginfo("Timed out achieving goal")
            else:
                # We made it!
                state = self.move_base.get_state()
                if state == GoalStatus.SUCCEEDED:
                    rospy.loginfo("Goal succeeded!")                 

    def shutdown(self):
        rospy.loginfo("Stopping the robot...")
        # Cancel any active goals
        self.move_base.cancel_goal()
        rospy.sleep(2)
        # Stop the robot
        self.cmd_vel_pub.publish(Twist())
        rospy.sleep(1)
 
def Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony):    
    rospy.wait_for_service('Final_ints')
    try:
        Final_ints = rospy.ServiceProxy('Final_ints', getwaypoint)
        resp1 = Final_ints(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)
        return resp1
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e

if __name__ == '__main__':
    try:
        MoveBaseAround()

    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
