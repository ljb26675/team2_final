#!/usr/bin/env python  
import roslib
import rospy
import math
import tf
import geometry_msgs.msg

from team2_final.srv import *
 
def Final_ints_client(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony):    
    rospy.wait_for_service('Final_ints')
    try:
        Final_ints = rospy.ServiceProxy('Final_ints', getwaypoint)

        resp1 = Final_ints(firstwp,symboldetected,symbolcolor,symbolpositionx,symbolpositiony)
        return resp1
    except rospy.ServiceException, e:
        print "Service call failed: %s"%e
'''
For right now, this just finds the robots position.
'''
if __name__ == '__main__':
    rospy.init_node('turtle_tf_listener')

    listener = tf.TransformListener()

    '''rospy.wait_for_service('spawn')
    spawner = rospy.ServiceProxy('spawn', turtlesim.srv.Spawn)
    spawner(4, 2, 0, 'turtle2')'''

    #turtle_vel = rospy.Publisher('turtle2/cmd_vel', geometry_msgs.msg.Twist,queue_size=1)

    rate = rospy.Rate(10.0)

    numWay = 0
    while (not rospy.is_shutdown()) and numWay<6 :
        try:
            (trans,rot) = listener.lookupTransform('/map', '/base_link', rospy.Time(0))
        except (tf.LookupException, tf.ConnectivityException, tf.ExtrapolationException):
            continue

        '''angular = 4 * math.atan2(trans[1], trans[0])
        linear = 0.5 * math.sqrt(trans[0] ** 2 + trans[1] ** 2)
        cmd = geometry_msgs.msg.Twist()
        cmd.linear.x = linear
        cmd.angular.z = angular'''
	#x = trans.getOrigin().x()
        #y = trans.getOrigin().y()
        #turtle_vel.publish(cmd)

	# prints x,y, rot or robot
	#print("X:", trans[0])
        #print("Y:", trans[1])
	print trans
       

	#first call

        rate.sleep()
