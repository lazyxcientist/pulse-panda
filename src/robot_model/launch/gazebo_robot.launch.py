import os
from os import pathsep
from ament_index_python.packages import get_package_share_directory, get_package_prefix

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.substitutions import Command, LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from pathlib import Path
import launch_ros

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue


def generate_launch_description():
    pkg_share = Path(launch_ros.substitutions.FindPackageShare(package='robot_model').find('robot_model'))
    default_model_path = pkg_share / 'urdf/robot.urdf'
    default_rviz_config_path = pkg_share / 'rviz/display.rviz'

    robot_description = get_package_share_directory("robot_model")
    robot_description_prefix = get_package_prefix("robot_model")
    gazebo_ros_dir = get_package_share_directory("gazebo_ros")

    model_arg = DeclareLaunchArgument(name="model", default_value=os.path.join(robot_description, "urdf", "robot.urdf.xacro"),description="Absolute path to robot urdf file")

    model_path = os.path.join(robot_description, "models")
    model_path += pathsep + os.path.join(robot_description_prefix, "share")

    env_var = SetEnvironmentVariable("GAZEBO_MODEL_PATH", model_path)

    robot_description = ParameterValue(Command(["xacro ", LaunchConfiguration("model")]),
                                       value_type=str)

    robot_state_publisher_node = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    start_gazebo_server = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, "launch", "gzserver.launch.py")
        ),
    )

    start_gazebo_client = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_dir, "launch", "gzclient.launch.py")
        )
    )




    ######################
    # gazebo_params_file = os.path.jovin(get_package_share_directory('core'),'config','gazebo_params.yaml')
    # gazebo_ros  =  IncludeLaunchDescription(
    #             PythonLaunchDescriptionSource([os.path.join(
    #                 get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')]),
    #                 launch_arguments={'extra_gazebo_args': '--ros-args --params-file ' + gazebo_params_file}.items()),
    #####################




    spawn_robot = Node(
                        package="gazebo_ros",
                        executable="spawn_entity.py",
                        arguments=["-entity", "Robot",
                                   "-topic", "robot_description",
                                    '-x', '0.0',
                                    '-y', '2.0',
                                    '-z', '0.0',
                                  ],
                        output="screen"
    )






    return LaunchDescription([
        env_var,
        model_arg,
        start_gazebo_server,
        start_gazebo_client,
        robot_state_publisher_node,
        # gazebo_ros,
        spawn_robot,



    # #####################################################
    # #####################################################
    # ############   to test the robot   ##################
    # DeclareLaunchArgument(
    #         name='rvizconfig',
    #         default_value=str(default_rviz_config_path),
    #         description='Absolute path to rviz config file',
    #     ),
    # # joint_state_publisher_node
    # Node(
    #     package='joint_state_publisher',
    #     executable='joint_state_publisher',
    #     name='joint_state_publisher',
    # ),
    # # joint_state_publisher_gui_node
    # Node(
    #     package='joint_state_publisher_gui',
    #     executable='joint_state_publisher_gui',
    #     name='joint_state_publisher_gui',
    # ),
    # # rviz_node
    # Node(
    #     package='rviz2',
    #     executable='rviz2',
    #     name='rviz2',
    #     output='screen',
    #     arguments=['-d', LaunchConfiguration('rvizconfig')],
    # )
    # #####################################################
    #####################################################
    #####################################################



    ])