import os

from ament_index_python.packages import get_package_share_directory

from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.conditions import IfCondition
from launch.conditions import UnlessCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch.substitutions import PathJoinSubstitution

from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare


def generate_launch_description():

    resources_package = 'robot_model'

    # Make path to resources dir without last package_name fragment.
    path_to_share_dir_clipped = ''.join(get_package_share_directory(resources_package).rsplit('/' + resources_package, 1))

    # Gazebo hint for resources.
    os.environ['GZ_SIM_RESOURCE_PATH'] = path_to_share_dir_clipped


    # Ensure `SDF_PATH` is populated since `sdformat_urdf` uses this rather
    # than `GZ_SIM_RESOURCE_PATH` to locate resources.
    if "GZ_SIM_RESOURCE_PATH" in os.environ:
        gz_sim_resource_path = os.environ["GZ_SIM_RESOURCE_PATH"]

        if "SDF_PATH" in os.environ:
            sdf_path = os.environ["SDF_PATH"]
            os.environ["SDF_PATH"] = sdf_path + ":" + gz_sim_resource_path
        else:
            os.environ["SDF_PATH"] = gz_sim_resource_path






    ##################################################
    ############## /load world files ##########################
    ##################################################
    default_world = os.path.join(
        get_package_share_directory('core'),
        'world',
        'empty.world'
        )    
    world = LaunchConfiguration('world')
    world_arg = DeclareLaunchArgument(
        'world',
        default_value=default_world,
        description='World to load'
        )
    ##################################################







    ##################################################
    ############ /Gazebo harmonic ####################
    ##################################################
    use_sim_time_launch_arg = DeclareLaunchArgument('use_sim_time', default_value='true')

    robot_discription = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([
            PathJoinSubstitution([
                FindPackageShare(resources_package),
                'launch',
                'display_robot.launch.py',
            ]),
        ]),
    )

    # Gazebo Sim.
    pkg_ros_gz_sim = get_package_share_directory('ros_gz_sim')
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_ros_gz_sim, 'launch', 'gz_sim.launch.py'),
        ),
        launch_arguments={'gz_args': ['-r -v4 ', world], 'on_exit_shutdown': 'true'}.items()
    )

    # Spawn
    spawn = Node(
            package='ros_gz_sim',
            executable='create',
            arguments=[
                '-name', 'robot.urdf',
                '-x', '1.2',
                '-z', '2.3',
                '-y', '1.4',
                '-topic', '/robot_description',
            ],
            output='screen',
    )
    #################################################









    ##################################################
    ############## /cmd_vel ##########################
    ##################################################
    bridge_params = os.path.join(get_package_share_directory('core'),'config','gz_bridge.yaml')
    ros_gz_bridge = Node(
        package="ros_gz_bridge",
        executable="parameter_bridge",
        arguments=[
            '--ros-args',
            '-p',
            f'config_file:={bridge_params}',
        ]
    )
    ros_gz_image_bridge = Node(
        package="ros_gz_image",
        executable="image_bridge",
        arguments=["/camera/image_raw"]
    )
    #####################################









    return LaunchDescription([
        use_sim_time_launch_arg,
        robot_discription,
        world_arg,
        gazebo,
        spawn,
        ros_gz_bridge,
        ros_gz_image_bridge,
    ])
