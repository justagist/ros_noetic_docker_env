import numpy as np
import quaternion

import rospy
from panda_robot import PandaArm

from geometry_msgs.msg import Pose, PoseStamped

# pub = rospy

poses = [
         [-8.48556818e-02, -8.88127666e-02, -6.59622769e-01, -1.57569726e+00, -4.82374882e-04,  2.15975946e+00,  4.36766917e-01],
         [ 1.34695728e-01, -2.74474940e-01, -2.46027836e-01, -1.19805447e+00, -5.27289847e-05,  2.17926193e+00,  9.10497957e-01],
         [ 1.81297444e-01,  3.94348774e-01, -2.25835923e-01, -1.19416311e+00, -7.51349249e-04,  2.79453565e+00,  8.36526167e-01],
         [ 0.63068724,      0.86207321,     -0.52113169,     -0.95186331,     0.02450696,       2.64150352,      0.5074312 ],
         [0.0, 0.0, 0.0, -0.0698, 0.0, 3.140, 00.785],
         [-0.0118073 ,  0.20327491, -0.04355536, -2.43355381,  0.01498074, 2.67250218,  0.64741629]
        ]

def create_pose_msg(ee_pose):
    pose = Pose()
    pose.position.x = ee_pose[0][0]
    pose.position.y = ee_pose[0][1]
    pose.position.z = ee_pose[0][2]

    pose.orientation.x = ee_pose[1].x
    pose.orientation.y = ee_pose[1].y
    pose.orientation.z = ee_pose[1].z
    pose.orientation.w = ee_pose[1].w

    # pose.header.frame = "world"

    msg = PoseStamped()
    msg.header.frame_id = "world"
    msg.pose = pose
    pub.publish(msg)
    
    return pose

def change_ori_pose_msg(msg, quat):
    msg.orientation.x = quat.x
    msg.orientation.y = quat.y
    msg.orientation.z = quat.z
    msg.orientation.w = quat.w

    return msg

def new_ori(quat1, quat2):

    return quaternion.from_rotation_matrix(quaternion.as_rotation_matrix(quat1)*quaternion.as_rotation_matrix(quat2))

if __name__ == '__main__':

    rospy.init_node("panda_env")

    pub = rospy.Publisher("/pose_test",PoseStamped,queue_size=10)
    
    r = PandaArm(reset_frames = True) # handle to use methods from PandaArm class
    fi = r.get_frames_interface() # frames interface object for the robot. Test switching EE frames
                                    # How to test: 
                                    # 1) open rviz -> add RobotModel (topic 'robot_description')
                                    # 2) set panda_link0 as global fixed frame
                                    # 3) add tf -> disable visualisation of all links except panda_EE
                                    # 4) run this script in terminal in interactive mode
                                    # 5) type $ fi.set_EE_frame_to_link('panda_hand')
                                    #       to move the EE frame to the link. Try different link names. 
                                    #       Test the same for the stiffness frame (set_K_frame_to_link)

    cm = r.get_controller_manager() # controller manager object to get controller states and switch controllers

    kin = r._kinematics # to test the kinematics (not required, can directly query kinematics using  methods in PandaArm)

    g = r.get_gripper() # gripper object. Test using $ g.close(), $ g.open(), $ g.home_joints(), $g.move_joints(0.01), etc.

    neutral = r.move_to_neutral 
    move_to = r.move_to_joint_position

    cpm = create_pose_msg
    v1 = [25.0, 25.0, 22.0, 20.0, 19.0, 17.0, 14.]
    v2 = [35.0, 35.0, 32.0, 30.0, 29.0, 27.0, 24.0]
    v3 = [30.0, 30.0, 30.0, 25.0, 25.0, 25.0]
    v4 = [40.0, 40.0, 40.0, 35.0, 35.0, 35.0]

    coll = r._collision_behaviour_interface
    # In interactive mode, for instance enter 
    #               $ neutral()
    #   to make the robot move to neutral pose
    # or type $ move_to(poses[0]) to move to the first joint pose from the list defined above (make sure robot workspace is free)

    mvt = r.get_movegroup_interface()

    q45x = quaternion.quaternion(0.924,0.383,0.,0.)
    q315x = quaternion.quaternion(0.924,-0.383,0.,0.)

    mtc = r.move_to_cartesian_pose

    pos, ori = r.ee_pose()

    # rate = rospy.Rate(10)

    # while not rospy.is_shutdown():
    #     print r.get_robot_status()['robot_mode']
    #     print ''
    #     rate.sleep()


