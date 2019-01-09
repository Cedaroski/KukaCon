#!/bin/bash

source devel/setup.bash &
roslaunch kinect2_bridge kinect2_bridge.launch &
sleep 2

rosrun kinect2_viewer icprunner
wait
exit 0

