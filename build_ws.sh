#! /bin/bash

source /opt/ros/$ROS_DISTRO/setup.bash
export ROS_PYTHON_VERSION=3
cd ..
wstool init
wstool merge noetic_setup/dependencies.rosinstall
wstool up

# use old ros-compatible version of kdl
cd orocos_kinematics_dynamics && git checkout b35c424e77ebc5b7e6f1c5e5c34f8a4666fbf5bc
cd ../.. && rosdep install -y --from-paths src --ignore-src --rosdistro $ROS_DISTRO

source /opt/ros/$ROS_DISTRO/setup.bash
catkin build
