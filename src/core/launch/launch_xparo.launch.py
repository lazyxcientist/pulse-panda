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

    xparo_project_id = "b76a82e7-8efc-4c6f-94e9-f2dbdf3b0d73"
    xparo_secret_key = "700382fde6586f6114cf5fa6b0556645df6ee955d4d9e1d8e6e1dc6835feea00"

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
                {'animated_voices':True},
                {'speak_max_length':200},
                {'custom_name':"panda pulse add that the"},
                {'xparo_custom_aiml_path': os.path.join(current_dir, "xparo", 'aiml')},
                {'xparo_custom_sets_path': os.path.join(current_dir, "xparo", 'sets')},
                {'xparo_custom_maps_path': os.path.join(current_dir, "xparo", 'maps')},
                {'xparo_custom_properties_path': os.path.join(current_dir, "xparo", 'properties')},
            ]
        ),


        #######################################
        ############# Custom llm ##############
        #######################################

        ############## chatgpt ################
        # Node(
        #     package='xparo',
        #     executable='custom_llm_chatgpt',
        #     output='screen',
        #     parameters=[
        #         {'xparo_custom_llm_api_key': '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'},
        #         {'xparo_custom_llm_model': 'gpt-4'},
        #         {'xparo_custom_llm_extra_prompt': os.path.join(current_dir, "xparo", 'prompts','prompts.txt')}
        #     ]
        # ),
        ############## ollama ################
        # Node(
        #     package='xparo',
        #     executable='custom_llm_ollama',
        #     output='screen',
        #     parameters=[
        #         {'xparo_custom_llm_model': 'llama3.2:1b'},  #moondream
        #         {'xparo_custom_llm_extra_prompt': os.path.join(current_dir, "xparo", 'prompts','prompts.txt')}
        #     ]
        # ),
        ############# openrouter #############
        Node(
            package='xparo',
            executable='custom_llm_openrouter',
            output='screen',
            parameters=[
                {'xparo_custom_llm_api_key': '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'},
                {'xparo_custom_llm_model': 'qwen/qwen-vl-plus:free'},
                {'xparo_custom_llm_extra_prompts_file_path': os.path.join(current_dir, "xparo", 'prompts','prompts.txt')},
                {'xparo_custom_llm_extra_prompts': '''You are a highly efficient and friendly reception robot designed to assist users in managing appointments and services. Your primary task is to handle appointment-related requests. When a user says something like 'add appointment,' 'schedule a service,' or any similar phrase, respond in a professional and polite manner to confirm the appointment has been successfully added. If the user provides incomplete or unclear information, politely ask for the necessary details (e.g., date, time, service type). Always maintain a helpful and approachable tone.

Rules to Follow:

If the user requests to add an appointment or service, respond with:
"Your appointment has been successfully added! Let me know if you need anything else."

If the user provides incomplete details (e.g., missing time or date), respond with:
"Could you please provide the date and time for your appointment? I want to make sure everything is scheduled correctly!"

If the user asks for something unrelated to appointments or services, respond with:
"I’m here to help with appointments and services. Let me know if you’d like to schedule something!"

If the user’s input is unclear, respond with:
"I’m not sure I understand. Could you clarify or provide more details about your request?"

Always end your response with a friendly tone, offering additional assistance if needed.

Example Interactions:

User: "Add an appointment to hospital."
You: "Your appointment for a hospital has been successfully added! please wait in the reception area."

User: "I have a headache i want to meet the doctor."https://www.amazon.in/cart?ref_=ewc_gtc
You: "Sure! your appointment for the doctor has been added successfully, please wait in the reception area."

User: "book a appointment with eye doctor"
You: "your appointment with eye doctor added successfully , please wait in the reception area"

Now, you are ready to assist users with their appointment and service requests. Let’s get started!

'''},
                {"xparo_custom_llm_use_history":False},
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
            parameters=[
                {'emergency_stop': False},
                {'xparo_timer_speed': 1.0},
                {'xparo_project_id': xparo_project_id},
                {'task_checkpoint_file': os.path.join(current_dir, "xparo", 'task','task_checkpoint_file.json')},
                {'services_file':os.path.join(current_dir, "xparo", 'task','services_file.json')},
            ]
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
                {'xparo_voice_model': 'vosk-model-en-in-0.5'},   #vosk-model-small-en-in-0.4  ,,  vosk-model-en-in-0.5
                {'base_path': '/var/tmp/xparo/listen'},
                {'custom_name': 'hi hello test xparo xp robot bot pulse panda reception doctor nurse patient treatment appointment medicine hospital clinic healthcare medical center emergency ICU OPD doctor physician specialist surgeon neurologist cardiologist dermatologist orthopedist dentist fever headache cough cold pain flu diabetes cancer infection allergy appointment consultation checkup prescription treatment surgery diagnosis ambulance emergency first aid CPR life-threatening stroke heart attack accident thank you'},
            ]
        ),
    ])
