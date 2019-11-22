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

  Create launch file to make world and bot and rviz
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
$
```



## NEED TO ADD VIDEO
