#! /bin/bash

# - Attach to a running docker container. ** Works only if one docker image is currently active!! **

shopt -s expand_aliases
source $HOME/.bashrc

command_exists () {
    type "$1" &> /dev/null ;
}

if command_exists nvidia-docker; then
      extra_params="--runtime nvidia"
      xdocker="nvidia-docker"
      echo -e "\t[INFO] nvidia-docker exists"
else
      xdocker="docker"
      extra_params="--device=/dev/dri:/dev/dri"
      echo -e "\t[INFO] nvidia-docker does not exist (falling back to docker). Rviz and Gazebo most likely will not work!"
fi

echo 'Entering container:' $1
$xdocker exec -it "$(docker ps -l -q)" bash
