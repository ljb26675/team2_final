#!/usr/bin/env python

from team2_final.srv import getwaypoint,getwaypointResponse
import rospy


Color = [2,1,3]
X =  [2,-1.5,-0.4]
Y = [2,1,5.7]

def handle_Final_ints(req):
    global i
    global X
    global Y
    if req.firstwp == True :
        i = 0 
        success = True
        waypointx = X[i]
        waypointy = Y[i]
        return getwaypointResponse(success,waypointx,waypointy)
    else:
        if req.symboldetected == True:
            if req.symbolcolor == Color[i] and abs(req.symbolpositionx - X[i]) < .001 and abs(req.symbolpositiony - Y[i]) < .001:
                success = True
		i = (i+1)%5           
            else:
                success = False
            waypointx = X[i]
            waypointy = Y[i]    
            return getwaypointResponse(success,waypointx,waypointy)
def Final_ints_server():
    global i 
    i = 0
    rospy.init_node('Final_ints_server')
    s = rospy.Service('Final_ints', getwaypoint, handle_Final_ints)
    print "Ready to go."
    rospy.spin()

if __name__ == "__main__":
    Final_ints_server()
