# CSCI 4530/6530 Final Project

## TEAM MEMBERS
Linsey Briley    UG
Nazish Tahir     G
Javier Rodriguez G


## TO RUN THIS PACKAGE

Make sure to catkin_make in catkin_ws dir to build package before inital use.

$ roscore

$ export HUSKY_GAZEBO_DESCRIPTION=$(rospack find husky_gazebo)/urdf/description.gazebo.xacro

$ export GAZEBO_MODEL_PATH=$(rospack find team2_final)/worlds

  Create launch file to make world and bot → final.launch
$ roslaunch team2_final final.launch

  launch rviz to see lazer/kinect data and rviz
$ roslaunch husky_viz view_robot.launch


## NEEDS TO BE UPDATED TO INCLUDE SERVICE, ETC

  launch gmapping/hector slam/amctl
$

  launch A-star
$

  launch computer vision
$



## NEED TO ADD VIDEO
