# CSCI 4530/6530 Final Project



## TEAM MEMBERS
Linsey Briley    UG
<br>
Nazish Tahir     G
<br>
Javier Rodriguez G
<br>

## Husky github
https://github.com/husky/husky

## TO RUN THIS PACKAGE

Make sure to ```catkin_make``` in *catkin_ws* dir to build package before inital use.
```
$ roscore

$ export HUSKY_GAZEBO_DESCRIPTION=$(rospack find husky_gazebo)/urdf/description.gazebo.xacro

$ export GAZEBO_MODEL_PATH=$(rospack find team2_final)/worlds
```

  Create launch file to make world and bot and rviz, and run the gmapping and move_base
<br>
```
$ roslaunch team2_final final.launch
```

## This makes the map
launch gmapping launch file from husky_navigation package 
<br>
```
$ roslaunch husky_navigation gmapping.launch
```
navigate husky around the world until you get satisfied with your map 
<br> 
```
$  rosrun teleop_twist_keyboard teleop_twist_keyboard.py
```
Save the map to disk
<br>
```
$ rosrun map_server map_saver -f <your map name>
```

## Navigation Manager starter code
  Run this to move the robot to some goal defined in the python file.
<br>
```
$ rosrun team2_final move_base_goal.py
```


## NEEDS TO BE UPDATED TO INCLUDE SERVICE, ETC

  launch gmapping/hector slam/amctl
<br>
```
$
```

  launch A-star
<br>
```
$
```
  launch computer vision
<br>
```
$ rosrun team2_final image_analysis.py
```

## Outside materials used
https://hotblackrobotics.github.io/en/blog/2018/01/29/action-client-py/
<br>
http://wiki.ros.org/navigation/Tutorials/SendingSimpleGoals
<br>
https://husarion.com/tutorials/ros-tutorials/7-path-planning/
<br>
https://husarion.com/tutorials/ros-tutorials/6-slam-navigation/#navigation-and-map-building
http://wiki.ros.org/ROS/Tutorials/DefiningCustomMessages
http://wiki.ros.org/opencv3
http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython


## NEED TO ADD VIDEO
