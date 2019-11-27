#!/usr/bin/env python
from __future__ import print_function

#import roslib
#roslib.load_manifest('package')
import sys
import rospy
import cv2
import numpy as np
from std_msgs.msg import String
from team2_final.msg import results
from sensor_msgs.msg import Image
from cv_bridge import CvBridge, CvBridgeError

cx = 0
cy = 0

class image_converter:

  def __init__(self):

    self.bridge = CvBridge()
    self.image_sub = rospy.Subscriber("/camera/rgb/image_raw",Image,self.callback)

  
  def callback(self,data):

    try:
      cv_image = self.bridge.imgmsg_to_cv2(data, "bgr8")
    except CvBridgeError as e:
      print(e)

    cv_gray = self.bridge.imgmsg_to_cv2(data, "mono8")
    #cv2.imshow("Orig", cv_image)
    #cv2.imshow("Gray", cv_gray)

    #split channels BGR image
    b,g,r = cv2.split(cv_image)

    #cv2.imshow("B", b)
    #cv2.imshow("G", g)
    #cv2.imshow("R", r)

    #find stars
    color = 0 
    area = 0
    contours = []
    #find contours on each channel
    b_sub = cv2.subtract(b, g)
    b_sub = cv2.subtract(b_sub, r)
    img_b, contours_b, hierarchy_b = cv2.findContours(b_sub, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    g_sub = cv2.subtract(g, b)
    g_sub = cv2.subtract(g_sub, r)
    img_g, contours_g, hierarchy_g = cv2.findContours(g_sub, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    r_sub = cv2.subtract(r, b)
    r_sub = cv2.subtract(r_sub, g)
    img_r, contours_r, hierarchy_r = cv2.findContours(r_sub, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    #cv2.imshow("B_", b_sub)
    #cv2.imshow("G_", g_sub)
    #cv2.imshow("R_", r_sub)

    detected = True
    if len(contours_b) > 0:
      contours += contours_b
      #color = 3
    if len(contours_g) > 0:
      contours += contours_g
      #color = 2
    if len(contours_r) > 0:
      contours += contours_r
      #color = 1
 
    #find the star (biggest contour area among all the contours)
    for i in range(0,len(contours)):
      if cv2.contourArea(contours[i]) > area:
        area = cv2.contourArea(contours[i])
        cnt = contours[i]
    #reject spurious areas
    if area > 50:
      #calculate Hu moments to find centroid of the star   
      M = cv2.moments(cnt) 
      #image Moments: Centroid is given by relations between M10, M00, and M01
      cx = int(M['m10']/M['m00'])
      cy = int(M['m01']/M['m00']) 
      #print('x = ',cx)
      #print('y = ',cy)

      #detect color of star (color of the centroid)
      #print(cv_image[cy,cx]) #images in OpenCV have inverted coordinates
      colorlevel = 0
      for j in range (0,3):
        if cv_image[cy,cx,j] > colorlevel:
          colorlevel = cv_image[cy,cx,j]
          color = 3 - j #OpenCV creates BGR images, and we assume server requires RGB images
      #print('color centroid = ', color)

      #show contours (just for debugging)
      #cv2.drawContours(cv_image, cnt, -1, (255,255,255), 2)
      #cv2.circle(cv_image, (cx,cy), 2, (255,255,255),-1)
      #cv2.imshow("Detected star", cv_image)
    
      #callback to calculate distance from the sensor to the star centroid using depth image
      self.image_depth = rospy.Subscriber("/camera/depth/image_raw",Image,self.callback_depth, (cx,cy)) 

    else:
      #print ("No star found")
      color = 0
      cx = 0
      cy = 0
      detected = False
     
    talker(self,detected, color, cx, cy)

    sys.exit()
    #cv2.waitKey()

  def callback_depth(self,data,args):
    #coordinates of the point to measure distance
    cx = args[0]
    cy = args[1]

    try:
      #read depth image from kinect sensor
      cv_depth = self.bridge.imgmsg_to_cv2(data)
    except CvBridgeError as e:
      print(e)
    #cv2.imshow("Depth Image", cv_depth)

    distance = cv_depth[cy,cx]
    #print('distance = ',distance)
    
def talker(self,detected,color,x,y):
  pub = rospy.Publisher('analysis', results, queue_size=1)
  #r = rospy.Rate(10) #10hz
  msg = results()
  msg.symboldetected = detected
  msg.symbolcolor = color
  msg.symbolpositionx = x
  msg.symbolpositiony = y
 
  #while not rospy.is_shutdown():
    #rospy.loginfo(msg)
  pub.publish(msg)
    #r.sleep()

def main(args):
  rospy.init_node('image_converter', anonymous=False)
  print("image_converter node initiated")
  ic = image_converter()
  try:
    rospy.spin()
  except KeyboardInterrupt:
    print("Shutting down")
    cv2.destroyAllWindows()

if __name__ == '__main__':
    main(sys.argv)
