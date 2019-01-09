
roslaunch kinect2_bridge kinect2_bridge.launch 
rosrun kinect2_viewer kinect2_viewer
rosrun kinect2_viewer icp

rosrun kinect2_bridge kinect2_bridge _fps_limit:=2
rosrun kinect2_calibration kinect2_calibration chess5x7x0.03 record color
source devel/setup.bash
rosrun kinect2_viewer icp ./InitPose/0000_cloud.pcd ./InitPose/InitPose.pcd 2

