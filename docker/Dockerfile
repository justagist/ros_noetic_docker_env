FROM osrf/ros:noetic-desktop-full
ENV DEBIAN_FRONTEND noninteractive

#ARG http_proxy
#ARG https_proxy

#ENV http_proxy=$http_proxy
#ENV https_proxy=$https_proxy

# install packages
RUN apt-get update && apt-get install -y --no-install-recommends \
    dirmngr \
    gnupg2 \
    && rm -rf /var/lib/apt/lists/*


#installs avahi for local network discovery (required for using the real robot)
RUN apt-get update && apt-get install -y \
    avahi-daemon avahi-utils


# Dependencies for baxter, sawyer and franka

RUN apt-get update && \ 
    apt-get -y install sudo nano python3-pip python3-scipy libprotobuf-dev protobuf-compiler libboost-all-dev \
                       ros-noetic-convex-decomposition ros-noetic-ivcon \
                       git-core python3-wstool python3-vcstools python3-rosdep ros-noetic-control-msgs \
                       ros-noetic-joystick-drivers ros-noetic-xacro ros-noetic-tf2-ros ros-noetic-rviz ros-noetic-cv-bridge \
                       ros-noetic-actionlib ros-noetic-actionlib-msgs ros-noetic-dynamic-reconfigure \
                       ros-noetic-trajectory-msgs ros-noetic-moveit \
                       ros-noetic-octomap-rviz-plugins \
                       ros-noetic-control-toolbox ros-noetic-catkin python3-catkin-tools \
                       ros-noetic-moveit-visual-tools \
                       ros-noetic-rospy-message-converter \
                       ros-noetic-realtime-tools ros-noetic-ros-controllers \
                       ros-noetic-tf-conversions ros-noetic-kdl-parser \ 
                       ros-noetic-ros-control ros-noetic-ros-controllers ros-noetic-gazebo-ros-control \
                       ros-noetic-libfranka \
                       build-essential python3-dev swig python3-pygame && \
    rm -rf /var/lib/apt/lists/*
 #ros-noetic-sns-ik-lib \

# RUN pip3 install --upgrade pip3 &&\
#     pip3 install protobuf && \
#     pip3 install pandas 


#six PySide
RUN pip3 install future numpy numpy-quaternion==2020.5.11.13.33.35 \
    pygame decorator matplotlib Pillow scipy scikit-learn osrf-pycommon


RUN if [[ $HTTP_PROXY != '' ]]; then git config --global http.proxy $HTTP_PROXY; fi

RUN apt-get update && apt-get -y install python3-catkin-tools
RUN apt-get update && apt-get -y upgrade

LABEL DEV_VERSION ros-noetic-dev

# disable sound card warnings in gazebo
COPY asound.conf /etc/asound.conf

# setup entrypoint, need entrypoint.sh in the same folder with Dockerfile
COPY ./ros_entrypoint.sh /
ENTRYPOINT ["/ros_entrypoint.sh"]

CMD ["bash"]