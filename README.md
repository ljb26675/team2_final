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

```
$ roscore

```

  Create launch file to make world and bot and rviz, and run the gmapping and move_base.
  This also exports the path to the models and the husky_gazebo_description.
  Also provides teleop for testing.
<br>
```
$ roslaunch team2_final final.launch
```

  Run the wpserver.py file
<br>
```
$ rosrun team2_final wpserver.py
```

  Run our image_analysis.py file, and to see it echo the /analysis topic
<br>
```
$ rosrun team2_final image_analysis.py

$ rostopic echo /analysis
```

  Run our ServiceManager.py file, and to see it echo the /service topic, but it also prints what its 
  seeing from /analysis. It won't publish until it sees a star.
<br>
```
$ rosrun team2_final ServiceManager.py

$ rostopic echo /service
```

  To launch astar:
<br>
```
$ roslaunch husky_navigation gmapping_astar_dwa.launch
```

  Run our move_base_around.py file, which should move the robot around with astar
<br>
```
$ rosrun team2_final move_base_around.py

```

  To save a version of our map, move around with the teleop keys, while clicked into 
  the terminal we launched with our launch file, then save the map to disk
<br>
```
$ rosrun map_server map_saver -f <your map name>
```


## Outside materials used
https://hotblackrobotics.github.io/en/blog/2018/01/29/action-client-py/
<br>
http://wiki.ros.org/navigation/Tutorials/SendingSimpleGoals
<br>
https://husarion.com/tutorials/ros-tutorials/7-path-planning/
<br>
https://husarion.com/tutorials/ros-tutorials/6-slam-navigation/#navigation-and-map-building
<br>
http://wiki.ros.org/ROS/Tutorials/DefiningCustomMessages
<br>
http://wiki.ros.org/opencv3
<br>
http://wiki.ros.org/cv_bridge/Tutorials/ConvertingBetweenROSImagesAndOpenCVImagesPython
<br>
https://docs.opencv.org/
<br> 
https://github.com/idincern/idincern-husky/tree/master/husky_navigation


## Video and screenshot of rviz after robot returns to 0,0 under the video/ directory

These are called video/FinalVideo.mp4 and video/rviz.png

## What we did

Image analysis script -> Image channels segmentation, find contours, select the biggest area and calculate centroid using Hu moments. Then analyze color of this particular pixel, and publish results to the /analysis topic. This script also calculate distance from the robot to the waal using the depth camera.
