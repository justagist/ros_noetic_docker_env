# ROS Noetic Docker Env

Docker image for testing code in Ubuntu 20.04 + ROS Noetic + Python 3 environment.

## Building image

Ideal required set up:

- Any Linux host (ideally Ubuntu)
- Docker and nvidia-docker ([Installation instructions](https://github.com/justagist/ros_noetic_docker_env/wiki))

To build image, run: `$ docker build docker/ -t noetic_env:dev`, or pull the pre-built image from github (`$ docker pull docker.pkg.github.com/justagist/ros_noetic_docker_env/noetic_env:v0.0.1`).

## Using container

Clone this repository. To run the built image interactively, run the script `$ ./run_docker.sh` from the cloned repository. The container starts in a shell where all your code can be tested.

Important points:

- The container starts in a catkin workspace at `/home/$USER/noetic_dev_ws` (original directory location in host machine: `/home/$USER/.noetic_dev_ws`).
- *This repository/directory* is mounted as `src/noetic_setup` in the container. Any change made to this repository outside the image is reflected inside as well (and vise-versa), just like all other mounted `rw` volumes (see `run_docker.sh`).
- (Warning: Also loads `/etc/sudoers/` as read-only for `sudo` usage without additional user configuration for docker. *This is probably not the best idea.*)
- **The host's home directory is also mounted in the container** for access to `.ros/` and for making the catkin workspace writable. To see and modify other mounted volumes, go through the `run_docker.sh` file. So all files in `$HOME` are accessible and **modifiable** from within the docker.

**When running for the first time, the catkin workspace has to be built: run `$ cd src/noetic_setup/ && ./build_ws.sh`. Once this is built successfully (fingers crossed!), source the workspace: `$ source $HOME/noetic_dev_ws/devel/setup.bash`. All the pre-built ROS packages and custom packages in `src` should now work.**

## Using same container in multiple terminals

To connect a new shell session to a currently active container, run `$ ./attach_container.sh`. This will start another instance of the same container in the same workspace at `/home/$USER/noetic_dev_ws`.

It might be worth it to add this script as an alias in your profile. To do that, add the following line in your `$HOME/.bashrc` file: `function newdockterm () { $HOME/workspace/ros_noetic_docker_env/attach_container.sh }`. (Note that this assumes that this repository was cloned to `$HOME/workspace/ros_noetic_docker_env`; replace this with the absolute path to wherever the repository is.) Once this is done, you can attach any new shell session to the currently active container by executing the command `$ newdockterm`.

**Note: Whenever a new shell session is connected, you need to source the catkin workspace: `$ source $HOME/noetic_dev_ws/devel/setup.bash`.**

### Testing catkin build

As mentioned above, when running the image using `$ ./run_docker.sh` for the first time, the catkin workspace has to be built by running `$ ./build_ws`. Once built and sourced, the installation can be tested as follows:

**Testing with Panda Simulator:**

This test will confirm whether the following are correctly installed and usable:

*Note: This **may** fail if you have not installed `nvidia-docker`.*

- ROS Noetic basic packages (msgs, controllers, actionlib, moveit, etc.)
- GL-based visualisation tools (RViz, Gazebo)
- Python 3 compatibility with ROS
- Attaching same docker container in multiple shell instances
- Your ability to follow instructions

To run the test:

1. Start simulator: `$ roslaunch panda_gazebo panda_world.launch`. This should start gazebo instance with a Franka Emika Panda robot in a neutral pose.
2. Open another terminal, and attach it to the currently active container by running `$ ./attach_container.sh` from this directory (or using the previously defined global command `$ newdockterm`). Make sure to source the workspace.
3. Start Moveit server for the simulated robot: `$ roslaunch panda_sim_moveit sim_move_group.launch`. This should start the moveit server; if correctly started, the terminal should show a message saying "You can start planning now!".
4. Open another terminal and attach it to the same container as well (Step 2). In this new session, run MoveIt demo via RViz: `$ roslaunch panda_simulator_examples demo_moveit.launch`: This should start RViz and an interactive MoveIt demo for the Panda robot. Move the goal marker, and click on "Plan and execute" in the "Planning" tab in RViz. The robot (in RViz and Gazebo) should plan and execute a motion to the new target. (*Note: If you want to replan or give a new target, you have to uncheck the "MotionPlanning" display in RViz, and then re-enable it before providing a new target; this is a bug in RViz.)

If all the above ran as desired, thank your lucky stars.

(This setup should also allow you to control the real Panda robot (Follow instructions from [Franka ROS Interface](https://github.com/justagist/franka_ros_interface))).
