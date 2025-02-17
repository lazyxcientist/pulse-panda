import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration
from launch_ros.actions import Node


def generate_launch_description():

    channel_type =  LaunchConfiguration('channel_type',     default='serial')
    serial_baudrate = LaunchConfiguration('serial_baudrate',default='115200')
    frame_id = LaunchConfiguration('frame_id',              default='laser_frame')
    inverted = LaunchConfiguration('inverted',              default='False')
    angle_compensate = LaunchConfiguration('angle_compensate',default='True')
    scan_mode = LaunchConfiguration('scan_mode',            default='Standard') #Sensitivity
    serial_lidar_port = LaunchConfiguration('serial_lidar_port',        default='/dev/ttyUSB3')
    serial_tyre_port = LaunchConfiguration('serial_tyre_port',        default='/dev/ttyACM0')
    serial_arm_port = LaunchConfiguration('serial_arm_port',        default='/dev/ttyACM1')
    serial_module_port = LaunchConfiguration('serial_module_port',        default='/dev/ttyACM2')
    use_sim_time = LaunchConfiguration('use_sim_time',        default='false')




    return LaunchDescription([

            ######################################
            #### parameters
            DeclareLaunchArgument('channel_type',   default_value=channel_type,description='Specifying channel type of lidar'),
            DeclareLaunchArgument('serial_baudrate',default_value=serial_baudrate,description='Specifying usb port baudrate to connected lidar'),
            DeclareLaunchArgument('frame_id',       default_value=frame_id,description='Specifying frame_id of lidar'),
            DeclareLaunchArgument('inverted',       default_value=inverted,description='Specifying whether or not to invert scan data'),
            DeclareLaunchArgument('angle_compensate',default_value=angle_compensate,description='Specifying whether or not to enable angle_compensate of scan data'),
            DeclareLaunchArgument('scan_mode',      default_value=scan_mode,description='Specifying scan mode of lidar'),
            DeclareLaunchArgument('serial_lidar_port',    default_value=serial_lidar_port,description='Specifying usb port to connected lidar'),
            DeclareLaunchArgument('serial_tyre_port',    default_value=serial_tyre_port,description='Specifying usb port to connected tyre base'),
            DeclareLaunchArgument('serial_arm_port',    default_value=serial_arm_port,description='Specifying usb port to connected arm'),
            DeclareLaunchArgument('serial_module_port',    default_value=serial_module_port,description='Specifying usb port to connected modules'),
            DeclareLaunchArgument('use_sim_time',    default_value=use_sim_time,description='Specifying use_sim_time'),











            ##############################################
            #### camera
        #     Node(
        #     		package='v4l2_camera',
        #     		executable='v4l2_camera_node',
        #     		output='screen',
        #     		namespace='camera',
        #     		# parameters=[{
        #     		# 	'image_size': [640, 480],
        #     		# 	'time_per_frame': [1, 6],
        #     		# 	'camera_frame_id': 'camera_link_optical'
        #     		# 	}]
        #     		),
        #### depth camera
        IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                        os.path.join(get_package_share_directory('realsense2_camera'),
                        'launch', 'rs_launch.py'))),

            ##############################################




















    ])
