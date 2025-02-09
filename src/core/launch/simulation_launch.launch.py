import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription, TimerAction,ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.actions import RegisterEventHandler,DeclareLaunchArgument
from launch.event_handlers import OnProcessStart
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition, UnlessCondition
from launch_ros.actions import Node



def generate_launch_description():

    package_name='core' 
    current_dir = get_package_share_directory(package_name)
    use_sim_time = LaunchConfiguration('use_sim_time',      default='true')




    return LaunchDescription([

            ######################################
            #### parameters
            DeclareLaunchArgument('use_sim_time',   default_value=use_sim_time ,description='Specifying whether or not to use simulation or real robot'),



            ##############################################
            ##############################################
            ##############################################
            # launch the robot
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('robot_model'),'launch',
                    # 'gazebo_robot.launch.py'  ## classic gazebo
                      'gazebo_ignition.launch.py'  ## ignition gazebo

                    )),
                    launch_arguments={
                        "world":os.path.join(get_package_share_directory('core'),'world',
                                             'empty.world'
                                             ),}.items()
            ),


            ##############################################
            ##############################################
            ##############################################







            ##############################################
            # launch controllers
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('robot_controller'),
                    'launch', 'controller.launch.py')),
                    launch_arguments={
                                        "use_sim_time":use_sim_time,
                                        "wheel_radius":"0.033",
                                        "wheel_separation":"0.17",
                                        "wheel_radius_error":"0.005",
                                        "wheel_separation_error":"0.02",
                                    }.items()
            ),



            # ##############################################
            # # # launch features
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('core'),
                    'launch', 'launch_features.launch.py')),
                    launch_arguments={
                                        "use_sim_time":use_sim_time,
                                    }.items()
            ),



            ##############################################
            # # # launch visvalization
            # IncludeLaunchDescription(
            #     PythonLaunchDescriptionSource(
            #         os.path.join(get_package_share_directory('core'),
            #         'launch', 'launch_data_visualization.launch.py')),
            # ),






    ])

