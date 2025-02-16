#!/usr/bin/env python3
import rclpy
import json
import re
import serial
import time
import random
import threading
import subprocess
import os
from rclpy.node import Node
from std_msgs.msg import String,Bool
import sounddevice as sd
import numpy as np
import wave
import os
from ament_index_python.packages import get_package_share_directory
from pydub import AudioSegment
from pydub.playback import play

base_path_for_package = get_package_share_directory('xparo_speak')



class Speak(Node):
    def __init__(self):
        super().__init__("speak")
        ################################################
        ########## for production purpose only #########
        try:
            with open(os.path.expanduser("~/xparo_config.json"), 'r') as file:
              xparo_config = json.load(file)
            self.get_logger().warning("ALERT: xparo_config.json file found in home directory. Using it for configuration.")
            self.get_logger().warning("we you are not in production mode. then delete the ~/xparo_config.json file.")
        except:
          xparo_config={}
        # xparo_config.get("", "")
        ################################################
        # parameters
        self.port=self.declare_parameter('port', xparo_config.get("port", "/dev/ttyUSB0")).get_parameter_value().string_value
        self.baud_rate=self.declare_parameter('baud_rate',xparo_config.get("baud_rate",9600 ) ).get_parameter_value().integer_value
        self.running =self.declare_parameter('running',xparo_config.get("running", False) )
        self.base_path =self.declare_parameter('speak_path',xparo_config.get("speak_path", "/var/tmp/xparo/speak") ).get_parameter_value().string_value
        self.emote_dict = {
    "neutral":{
        "sound":"gbaby_quick_suprise.wav",
        "animation": "happy",
        },
    "happy":{
        "sound":"gbaby_giggle.wav",
        "animation": "happy"
        },
    "sad":{
        "sound":"gbaby_wakeup.wav",
        "animation": "sad"
        },
    "close":{
        "sound":"gbaby_quick_suprise_5.wav",
        "animation": "close"
        },
    "angry":{
        "sound":"gbaby_yummy.wav",
        "animation": "angry"
        },
    "confused":{
        "sound":"gbaby_haah.wav",
        "animation": "confused"
        },
    "suspicious":{
        "sound":"gbaby_quick_suprise_2.wav",
        "animation": "suspicious"
        },
    "pain":{
        "sound":"gbaby_wakeup.wav",
        "animation": "pain"
        },
    "unamused":{
        "sound":"gbaby_hay.wav",
        "animation": "unamused"
        },
    "unsure":{
        "sound":"gbaby_he.wav",
        "animation": "unsure"
        },
    "charger_connected":{
        "sound":"charger_connected.wav",
        "animation": "charger_connected"
        },
}
        self.emotion_patterns = {
            "happy": re.compile(r"\b(happy|joy|excited|glad|cheerful|elated|content|joyful|happiness|delighted|ecstatic|satisfied|pleased|optimistic|bright|upbeat|good|awesome|wonderful|fantastic|beaming|smiling|grinning|laughing)\b", re.IGNORECASE),
            "sad": re.compile(r"\b(sad|unhappy|down|sorrow|mourn|saddened|depressed|blue|disappointed|dismal|gloomy|melancholy|heartbroken|desolate|despondent|grieving|grief)\b", re.IGNORECASE),
            "angry": re.compile(r"\b(angry|rage|furious|mad|irritated|irate|fuming|enraged|outraged|vexed|livid|wrath|frustrated|displeased|annoyed|upset|infuriated|wrathful|exasperated)\b", re.IGNORECASE),
            "confused": re.compile(r"\b(confused|puzzled|lost|uncertain|foggy|bewildered|disoriented|baffled|perplexed|mixed|muddled|discombobulated|flustered)\b", re.IGNORECASE),
            "surprised": re.compile(r"\b(surprised|shocked|amazed|stunned|astonished|startled|dumbfounded|flabbergasted|speechless|taken aback|unexpected)\b", re.IGNORECASE),
            "fear": re.compile(r"\b(fear|scared|afraid|terrified|panic|anxious|nervous|alarmed|frightened|horrified|horrible|uneasy|disturbed|paranoid|dread)\b", re.IGNORECASE),
            "bored": re.compile(r"\b(bored|tired|indifferent|disinterested|apathetic|listless|unmotivated|uninspired|bland|unenthused|weary|unexcited)\b", re.IGNORECASE),
            "excited": re.compile(r"\b(excited|enthusiastic|eager|pumped|thrilled|exhilarated|elated|ecstatic|fired up|zealous|charged up)\b", re.IGNORECASE),
            "anxious": re.compile(r"\b(anxious|nervous|uneasy|worried|concerned|apprehensive|restless|on edge|fretful|troubled|tense|stressed|nervy)\b", re.IGNORECASE),
            "neutral": re.compile(r"\b(hello|hi|okay|fine|thanks|fine|just|nothing much|what’s up|alright|sure|okay|yeah|nothing)\b", re.IGNORECASE),
        }
        self.animation_duration = (5, 10)  # Animation duration range in seconds
        self.lock = threading.Lock()


        # topics
        self.create_subscription(String, '/xparo/response', self.animate_now, 10)
        self.xparo_send = self.create_publisher(String, '/xparo/dashboard/send', 10)
        self.xparo_send_sub = self.create_subscription(String, '/xparo/dashboard/send', self.dashboard_send, 10)
        self.pir_detected = self.create_publisher(Bool, '/xparo/sensor/PIR', 10)
        self.pir_detected_default = False


        # self.base_path = "/var/tmp/xparo/speak"
        if not os.path.exists(self.base_path):
            os.makedirs(self.base_path)
        
        ## PIR feature #TODO: not stable now 
        try:
            self.connect()
        except Exception as e:
            self.get_logger().error(f"Failed to connect to Arduino: {e}")
            try:
                self.port="/dev/ttyUSB0"
                self.connect()
            except:
                try:
                    self.port="/dev/ttyUSB1"
                    self.connect()
                except:
                    try:
                        self.port="/dev/ttyACM0"
                        self.connect()
                    except:
                        try:
                            self.port="/dev/ttyACM1"
                            self.connect()
                        except:
                            pass

                


    def connect(self):
        self.arduino = serial.Serial(str(self.port), self.baud_rate, timeout=1)
        if self.arduino.is_open:
            print("Connected to Arduino")
            self.start_pir_monitoring()
        else:
            print("Failed to connect to Arduino")


    ############################################################
    ############################################################
    ############################################################

    def animate_now(self, message):
        text = str(message.data)
        try:
            dta = json.loads(text)
            text = dta["xparo"]
        except:
            pass
        ###############
        qq = String()
        qq.data = json.dumps({"emotion":self.detect_emotion(text)})
        # self.xparo_send.publish(qq)
        self.dashboard_send(qq)


    def stop_existing_playback(self):
        try:
            subprocess.run(['pkill', '-f', 'aplay'], check=True)
        except subprocess.CalledProcessError:
            pass


    def play_audio(self,file_path=None):
        if file_path is None:
            file_path = os.path.join(self.base_path,"tts_adjusted.wav")
        
        # device_info = sd.query_devices(kind='output')
        # print(f"Available output devices: {device_info}")
        # sound = AudioSegment.from_file(file_path)
        # play(sound)


        try:
            directory = os.path.join(get_package_share_directory("xparo_speak"),"sound")
            os.system(f"aplay {os.path.join(directory, file_path)}")
        except Exception as e:
            print(e)

        
    ############################################################
    ############################################################
    ############################################################

    def detect_emotion(self, text):
        text = str(text).lower()
        for emotion, pattern in self.emotion_patterns.items():
            if pattern.search(text):
                return emotion  # Return the first matching emotion
        return "happy"

    def dashboard_send(self,msg):
        self.get_logger().error(f"dashbaord send is called {msg.data}")
        try:
            dataa = json.loads(msg.data.replace("'", "\""))
            self.get_logger().info(f"dash send {dataa}")
            for ii ,jj in dataa.items():
                if ii == "emotion":
                    self.play_animation(jj)
        except json.JSONDecodeError as e:
            print(f"JSON decode error: {e}: {msg.data}")


    def send_command(self, data):
        command = f"{data}\n"
        if self.arduino.is_open:
            self.arduino.write(command.encode("utf-8"))
            time.sleep(0.02)


    def read_pir(self):
        while True:
            if self.arduino.in_waiting > 0:
                line = self.arduino.readline().decode("utf-8").strip()
                if line.startswith("PIR:"):
                    pir_value = int(line.split(":")[1])
                    with self.lock:
                        temp_pir_value = self.pir_detected_default
                        if pir_value >= 0.6:
                            temp_pir_value = True
                        else:
                            temp_pir_value = False

                        if self.pir_detected_default!=temp_pir_value:
                            ss = Bool()
                            ss.data = self.pir_detected_default
                            self.pir_detected.publish(ss)


    def start_pir_monitoring(self):
        pir_thread = threading.Thread(target=self.read_pir, daemon=True)
        pir_thread.start()



    ############################################################
    ############################################################
    ############################################################

    def play_animation(self, emotion):
        """
        Plays the animation corresponding to the given emotion.
        """
        # if self.running  or ( emotion not in self.emote_dict ):
        #     return

        animation_func = self.emote_dict[emotion]["animation"]
        sound_file = self.emote_dict[emotion]["sound"]
        self.play_audio(sound_file)

        # self.running = True
        # duration = random.randint(*self.animation_duration)
        # print(f"Playing '{emotion}' animation with sound {sound_file} for {duration} seconds.")
        # animation_thread = threading.Thread(target=animation_func, args=(duration,))
        # animation_thread.start()
        # animation_thread.join()
        # self.running = False

        self.send_command(animation_func)




    def close(self):
        if self.arduino.is_open:
            self.arduino.close()





def main(args=None):
    rclpy.init(args=args)
    speak = Speak()
    try:
        rclpy.spin(speak)
    except KeyboardInterrupt:
        pass
    speak.destroy_node()
    rclpy.try_shutdown()


if __name__ == '__main__':
    main()
