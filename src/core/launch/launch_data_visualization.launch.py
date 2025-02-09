import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from pathlib import Path
import launch_ros

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue



def generate_launch_description():

    pkg_share = Path(launch_ros.substitutions.FindPackageShare(package='robot_model').find('robot_model'))
    use_sim_time = LaunchConfiguration('use_sim_time',      default='True')
    visualize_data = LaunchConfiguration('visualize_data',  default='True')
    default_rviz_config_path = pkg_share / 'rviz/display.rviz'




    return LaunchDescription([

            ######################################
            #### parameters
            DeclareLaunchArgument('use_sim_time',   default_value=use_sim_time,description='Specifying whether or not to use simulation or real robot'),
            DeclareLaunchArgument('visualize_data',      default_value=visualize_data,description='Specifying visualize the robot'),

                DeclareLaunchArgument(
                        name='rvizconfig',
                        default_value=str(default_rviz_config_path),
                        description='Absolute path to rviz config file',
                        ),



            ##############################################
            ############  data visualization   ##########
            ##############################################
            # rviz2 
                Node(
                        package='rviz2',
                        executable='rviz2',
                        name='rviz2',
                        output='screen',
                        arguments=['-d', LaunchConfiguration('rvizconfig')],
                ),
            # # rqt
            # ExecuteProcess(cmd=['rqt']),
            # # plotjuggler
            # Node(
            #         package='plotjuggler',
            #         executable='plotjuggler',
            #         name='plotjuggler_data_plot',
            #         output='screen'
            #     ),
            # # 

            # # joint control publisher
            # Node(
            #     package="joint_state_publisher_gui",
            #     executable="joint_state_publisher_gui"
            # ),
            ##############################################





    ])
