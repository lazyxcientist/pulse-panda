from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, GroupAction, OpaqueFunction
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.conditions import UnlessCondition, IfCondition
from ament_index_python.packages import get_package_share_directory
from launch.actions import IncludeLaunchDescription, TimerAction,ExecuteProcess
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command
from launch.actions import RegisterEventHandler
from launch.event_handlers import OnProcessStart
import os








def generate_launch_description():
    ## launch configuration
    wheel_radius =              LaunchConfiguration("wheel_radius",           default="0.033")
    wheel_separation =          LaunchConfiguration("wheel_separation",       default="0.17")
    wheel_radius_error =        LaunchConfiguration("wheel_radius_error",     default="0.005")
    wheel_separation_error =    LaunchConfiguration("wheel_separation_error", default="0.02")
    use_sim_time =              LaunchConfiguration('use_sim_time',           default='false')




    ###############################################
    # # ros2 controller 
    robot_description = Command(['ros2 ', ' param ', ' get ', ' --hide-type ', ' /robot_state_publisher ', ' robot_description '])
    controller_params_file = os.path.join(get_package_share_directory('robot_controller'),'config','my_controllers.yaml')
    controller_manager = Node(
                                    package="controller_manager",
                                    executable="ros2_control_node",
                                    parameters=[
                                                    {'robot_description': robot_description},
                                                    controller_params_file
                                                ]
                                )
    ###############################################





    ###############################################
    # joint state broadcaster
    joint_state_broadcaster_spawner = Node(
                                            package="controller_manager",
                                            executable="spawner",
                                            arguments=["joint_broad"],
                                        )
    # wheel controllers bradcaster
    wheel_controller_spawner = Node(
                                        package="controller_manager",
                                        executable="spawner",
                                        arguments=["diff_cont"],
                                    )
    ###############################################








    ###############################################
    ###############################################
    launch_dis_extension = []
    # if False:
    #     print("sim time is true -------------------------------")
    #     launch_dis_extension += [
    #         joint_state_broadcaster_spawner,
    #         wheel_controller_spawner,
    #     ]
    # else:
    #     print('NOT sim time -----------------------------')
    #     launch_dis_extension += [
    #         ## delayed controllers
    #         TimerAction(period=3.0, 
    #                     actions=[controller_manager],
    #                     # condition=UnlessCondition(use_sim_time)
    #                     ),
    #         RegisterEventHandler(event_handler=OnProcessStart(target_action=controller_manager,
    #                             on_start=[joint_state_broadcaster_spawner],)),
    #         RegisterEventHandler(event_handler=OnProcessStart(target_action=controller_manager,
    #                             on_start=[wheel_controller_spawner],)),
    #     ]
    ###############################################
    ###############################################







    return LaunchDescription(
        [
            ## launch argument
            DeclareLaunchArgument("wheel_radius",           default_value=wheel_radius),
            DeclareLaunchArgument("wheel_separation",       default_value=wheel_separation,),
            DeclareLaunchArgument("wheel_radius_error",     default_value=wheel_radius_error),
            DeclareLaunchArgument("wheel_separation_error", default_value=wheel_separation_error),
            DeclareLaunchArgument('use_sim_time',   default_value=use_sim_time,description='Specifying whether or not to use simulation or real robot'),



            # joint_state_broadcaster_spawner,
            # wheel_controller_spawner,

            ## delayed controllers
            TimerAction(period=3.0, 
                        actions=[controller_manager],
                        # condition=UnlessCondition(use_sim_time)
                        ),
            RegisterEventHandler(event_handler=OnProcessStart(target_action=controller_manager,
                                on_start=[joint_state_broadcaster_spawner],),
                                            # condition=UnlessCondition(use_sim_time)
                                            ),
            RegisterEventHandler(event_handler=OnProcessStart(target_action=controller_manager,
                                on_start=[wheel_controller_spawner],),
                                            # condition=UnlessCondition(use_sim_time)
                                            ),



        ]+launch_dis_extension
    )