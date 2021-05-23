#! /bin/bash
ROOT_DIR="$(cd $( dirname ${BASH_SOURCE[0]} ) && pwd)"

command_exists () {
    type "$1" &> /dev/null ;
}

# path where the catkin ws will be stored for the docker to use
HOST_WS_PATH="$HOME/.noetic_dev_ws"

if command_exists nvidia-docker; then
      extra_params="--runtime nvidia"
      xdocker="nvidia-docker"
      echo -e "\t[INFO] nvidia-docker exists"
else
      xdocker="docker"
      extra_params="--device=/dev/dri:/dev/dri"
      echo -e "\t[INFO] nvidia-docker does not exist (falling back to docker). Rviz and Gazebo most likely will not work!"
fi

IMAGE_NAME=`docker images -f "label=DEV_VERSION=ros-noetic-dev" -q`
IMAGE_NAME=($IMAGE_NAME dummy) # make it into list for dealing with single and multiple entry from above output

echo -e "\n\t[STATUS] Loading image: ${IMAGE_NAME[0]} ..."

if ! [ -d "${HOST_WS_PATH}/src" ]; then
    mkdir -p ${HOST_WS_PATH}/src
fi

$xdocker run -it \
       --user=$(id -u) \
       --env="DISPLAY" \
       --network="host" \
       --ulimit rtprio=99 \
       --cap-add=sys_nice \
       --privileged \
       --env="QT_X11_NO_MITSHM=1" \
       --volume="/home/$USER:/home/$USER" \
       --volume="/etc/group:/etc/group:ro" \
       --volume="/etc/passwd:/etc/passwd:ro" \
       --volume="/etc/shadow:/etc/shadow:ro" \
       --volume="/etc/sudoers.d:/etc/sudoers.d:ro" \
       --volume="/tmp/.X11-unix:/tmp/.X11-unix:rw" \
       --volume="${HOST_WS_PATH}:/home/$USER/noetic_dev_ws" \
       --volume="${ROOT_DIR}:/home/$USER/noetic_dev_ws/src/noetic_setup" ${extra_params} \
       --workdir="/home/$USER/noetic_dev_ws/" \
       ${IMAGE_NAME[0]} \
       bash 

rm -rf $HOME/noetic_dev_ws
echo -e "\nBye the byee!\n"
