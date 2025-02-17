import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription, ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node
from launch.conditions import IfCondition, UnlessCondition



def generate_launch_description():
    package_name='core'
    current_dir = get_package_share_directory(package_name)
    use_sim_time = LaunchConfiguration('use_sim_time', default='true')


 
    return LaunchDescription([
            DeclareLaunchArgument('use_sim_time',   default_value=use_sim_time ,description='Specifying whether or not to use simulation or real robot'),




            ##############################################
            ############ Xparo  ############
            ##############################################

            #  hardware
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('core'),
                    'launch', 'launch_hardware.launch.py'))
                    ),



            # xparo services
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(get_package_share_directory('core'),
                    'launch', 'launch_xparo.launch.py'))
                    ),

            ##############################################


            # background service
            Node(
                package='bot_workflow',
                executable='background_service',
                output='screen',
                parameters=[
                    {'service_url': 'https://lazy-legends-robotics.azurewebsites.net/'},
                    {'service_api': 'chatbot_api/pankaj/c736f428-d21c-47c4-8471-c16fc95701d0/'},
                ]),


            # background service
            Node(
                package='arduino_animate',
                executable='animate',
                output='screen',
                parameters=[
                    {'port': '/dev/ttyUSB0'},
                    {'baud_rate': 9600},
                    {'running':False},
                ]),






    ])
