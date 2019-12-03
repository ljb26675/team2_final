#!/usr/bin/env python
import rospy
import sys

from team2_final.srv import *
# Brings in the SimpleActionClient
import actionlib
# Brings in the .action file and messages used by the move base action
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from geometry_msgs.msg import Point
from std_msgs.msg import Float32
from team2_final.msg import results
'''
This ServiceManager file suscribes to /analysis topic and publishes the found goal from the service to the 
/service topic.
'''

init = True

point = Point(0,0,0)


''' 
    This defines a call to our service, where:
    firstwp: bool, set to True if first call
    symboldetected: bool, set to True if detected symbol
    symbolcolor: int, 1 - Red, 2 - Green, 3 - Blue, else invalid  
    symbolpositionx, symbolpositiony: x,y float of position of current symbol
'''
def Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony):    
    rospy.wait_for_service('Final_ints')
    try:
        Final_ints = rospy.ServiceProxy('Final_ints', getwaypoint)

        resp1 = Final_ints(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)
        return resp1
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e


'''
	Callback function fo when it hears data
'''
def callback(data):
    rospy.loginfo(rospy.get_caller_id() + "I heard %s", data.symboldetected)
    '''
    #make initial call 
    if init:
        #intial call to service, ideally we want symbolcolor from vision and symbol position from the last call to the service
	firstwp = bool(True)
        symboldetected = bool(data.symboldetected)
        symbolcolor = int(1) 
        symbolpositionx = float(0)
        symbolpositiony = float(0)
	init = False
    else:
	firstwp = bool(False)
        symboldetected = bool(True)
        symbolcolor = int(data.data) 
        symbolpositionx = float(p.waypointx)
        symbolpositiony = float(p.waypointy)
    '''
    if data.symboldetected: 

        #intial call to service, ideally we want symbolcolor from vision and symbol position from the last call to the service
        global init
        print("Init", init)
        firstwp = bool(init)
        symboldetected = bool(data.symboldetected)
        symbolcolor = int(data.symbolcolor) 
        symbolpositionx = float(point.x)
        symbolpositiony = float(point.y)
        init = False

    
        p = Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)
        print "%s"%p

        global point
        print("Point", point)
        point = Point(p.waypointx, p.waypointy,0)
        pub.publish(point)

# If the python node is executed as main process (sourced directly)
if __name__ == '__main__':
    # Initializes a rospy node to let the SimpleActionClient publish and subscribe
    rospy.init_node('service_manager')
   
    #make it subscribe to /vision
    sub = rospy.Subscriber('analysis', results, callback)

    #make it publish to a node called /service
    pub = rospy.Publisher('service', Point, queue_size=10)

    print("Service manager is running")

    rospy.spin()

