#!/usr/bin/env python
# license removed for brevity

import rospy

# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from team2_final.srv import *

def movebase_client(x,y,w):

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
   # No rotation of the mobile base frame w.r.t. map frame
    goal.target_pose.pose.orientation.w = w

   # Sends the goal to the action server.
    client.send_goal(goal)
   # Waits for the server to finish performing the action.
    wait = client.wait_for_result()
   # If the result doesn't arrive, assume the Server is not available
    if not wait:
        rospy.logerr("Action server not available!")
        rospy.signal_shutdown("Action server not available!")
    else:
    # Result of executing the action
        return client.get_result()   

def Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony):    
    rospy.wait_for_service('Final_ints')
    try:
        Final_ints = rospy.ServiceProxy('Final_ints', getwaypoint)

        resp1 = Final_ints(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)
        return resp1
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    try:
       # Initializes a rospy node to let the SimpleActionClient publish and subscribe
        rospy.init_node('movebase_client_py')

	#first call

        print("Moving to 2,2")
	firstwp = bool(True)
        symboldetected = bool(True)
        symbolcolor = int(2)
        symbolpositionx = float(0)
        symbolpositiony = float(0)
        result = Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)

	print(result)
        r = movebase_client(result.waypointx, result.waypointy, 90)

	print("Green Star detected, moving to next star")

	firstwp = bool(False)
        symboldetected = bool(True)
        symbolcolor = int(2) #green
        symbolpositionx = float(result.waypointx)
        symbolpositiony = float(result.waypointy)
        result = Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)

	print(result)
        r = movebase_client(result.waypointx, result.waypointy+1)

	print("Red Star detected, moving to next star")

	firstwp = bool(False)
        symboldetected = bool(True)
        symbolcolor = int(1) #red
        symbolpositionx = float(result.waypointx)
        symbolpositiony = float(result.waypointy)
        result = Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)

	print(result)
        r = movebase_client(result.waypointx, result.waypointy+1)

        print("Blue Star detected, moving to 0,0")

        '''
        firstwp = bool(False)
        symboldetected = bool(True)
        symbolcolor = int(e) #blue
        symbolpositionx = float(result.waypointx)
        symbolpositiony = float(result.waypointy)
        result = Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)

	print(result)
        r = movebase_client(result.waypointx+1, result.waypointy)


        print("Blue Star detected, moving to next star")

	firstwp = bool(False)
        symboldetected = bool(True)
        symbolcolor = int(3) #blue
        symbolpositionx = float(result.waypointx)
        symbolpositiony = float(result.waypointy)
        result = Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)

	print(result)
        r = movebase_client(result.waypointx, result.waypointy+1)

        '''

        if r:
            rospy.loginfo("Goal execution done!")
    except rospy.ROSInterruptException:
        rospy.loginfo("Navigation test finished.")
