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


            ##################################################
            ############## /cmd_vel ##########################
            ##################################################
            IncludeLaunchDescription(
                        PythonLaunchDescriptionSource([os.path.join(
                            get_package_share_directory(package_name),'launch','joystick.launch.py'
                        )]), launch_arguments={'use_sim_time': use_sim_time}.items()
            ),
            Node(
                    package="twist_mux",
                    executable="twist_mux",
                    parameters=[
                            os.path.join(get_package_share_directory('core'),'config','twist_mux.yaml'),
                            {'use_sim_time': use_sim_time}
                            ],
                    remappings=[('/cmd_vel_out','/diff_cont/cmd_vel_unstamped')]
                ),
            ####################################################




            ##############################################
            ############ Navigation 2 stack  ############
            ##############################################
            #launching slam_toolbox  to genrate slam map
            # IncludeLaunchDescription(
            #     PythonLaunchDescriptionSource(
            #         os.path.join(get_package_share_directory('slam_toolbox'), #slam_toolbox
            #         'launch', 'online_async_launch.py')),
            #         launch_arguments={
            #                         'params_file': os.path.join(current_dir,'config','mapper_params_online_async.yaml'),
            #                         'use_sim_time':use_sim_time
            #                         }.items()
            #         ),



            # # ## loading AMCL localization
            # IncludeLaunchDescription(
            #     PythonLaunchDescriptionSource(
            #         os.path.join(get_package_share_directory('nav2_bringup'), #nav2_bringup
            #         'launch', 'localization_launch.py')),
            #         launch_arguments={
            #                         'map': os.path.join(current_dir,'maps','testing_world_map.yaml'),
            #                         'use_sim_time':use_sim_time,
            #                         'map_subscribe_transient_local':'true'}.items()
            #         ),


            ## loading nav2 stack
            ## ros2 launch nav2_bringup navigation_launch.py use_sim_time:=true
            # IncludeLaunchDescription(
            #     PythonLaunchDescriptionSource(
            #         os.path.join(get_package_share_directory('nav2_bringup'), #nav2_bringup
            #         'launch', 'navigation_launch.py')),
            #         launch_arguments={
            #             #  'map_subscribe_transient_local':'true',
            #                         'use_sim_time':use_sim_time}.items()
            #         ),
            # ExecuteProcess(
            #     cmd=[
            #         'ros2', 'launch', 'nav2_bringup', 'navigation_launch.py',
            #         f'use_sim_time:={use_sim_time}',
            #         # 'map_subscribe_transient_local:=true',
            #         # 'params_file:=' + os.path.join(current_dir, 'config', 'nav2_params.yaml')
            #     ]
            # ),
            ##############################################








    ])
