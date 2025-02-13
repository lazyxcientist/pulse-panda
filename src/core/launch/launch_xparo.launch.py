import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration

def generate_launch_description():
    package_name = 'core'
    current_dir = get_package_share_directory(package_name)
    use_sim_time = LaunchConfiguration('use_sim_time', default='True')

    xparo_project_id = "87d0e7da-9a6f-44a9-b163-2d36ea40614a"
    xparo_secret_key = "e9747ff149e9fb7a552cd4ddf05959692feab62986ce8b4fcc3df2e51b4706df"

    return LaunchDescription([
        # Declare Launch Arguments
        DeclareLaunchArgument('use_sim_time', default_value='True', description='Use simulation time'),

        # Xparo Brain
        Node(
            package='xparo',
            executable='xparo',
            name='xparo_ros',
            output='screen',
            parameters=[
                {'xparo_secret_key': xparo_secret_key},
                {'xparo_project_id': xparo_project_id},
                {'xparo_connection_type': 'hybrid'},
                {'xparo_custom_aiml_path': os.path.join(current_dir, "xparo", 'aiml')},
                {'xparo_custom_sets_path': os.path.join(current_dir, "xparo", 'sets')},
                {'xparo_custom_maps_path': os.path.join(current_dir, "xparo", 'maps')},
                {'xparo_custom_properties_path': os.path.join(current_dir, "xparo", 'properties')},
            ]
        ),

        # Dashboard UI
        Node(
            package='xparo_dashboard',
            executable='dashboard',
            name='xparo_dashboard',
            output='screen',
            parameters=[
                {'debug': True},
                {'xparo_project_id': xparo_project_id},
                {'xparo_dashboard_html_files_path': os.path.join(current_dir, "xparo", 'templates')},
                {'speak_path':os.path.join(current_dir, "xparo", 'speak')},
            ]
        ),

        # Settings
        Node(
            package='xparo_settings',
            executable='settings',
            name='xparo_settings',
            output='screen',
            parameters=[
                {'wifi_module': 'wlan0'},
                {'display_brightness_multiple': 960},
            ]
        ),

        # Task Management and Services
        Node(
            package='xparo_task',
            executable='task',
            name='xparo_task',
            output='screen',
        ),

        # Offline Speaking
        Node(
            package='xparo_speak',
            executable='speak',
            name='xparo_speak',
            output='screen',
            parameters=[
                {'tts_engine': 'pico'},
                {'port': '/dev/ttyUSB0'},
                {'baud_rate': 9600},
                {'speak_path': '/var/tmp/xparo/speak'},
            ]
        ),

        # Offline Listening
        Node(
            package='xparo_listen',
            executable='listen',
            name='xparo_listen',
            output='screen',
            parameters=[
                {'xparo_voice_model': 'vosk-model-small-en-in-0.4'},
                {'base_path': '/var/tmp/xparo/listen'},
            ]
        ),
    ])
