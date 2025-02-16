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
        self.port=self.declare_parameter('port', xparo_config.get("port", "/dev/ttyUSB0"))
        self.baud_rate=self.declare_parameter('baud_rate',xparo_config.get("baud_rate",9600 ) )
        self.running =self.declare_parameter('running',xparo_config.get("running", False) )
        self.base_path =self.declare_parameter('speak_path',xparo_config.get("speak_path", "/var/tmp/xparo/speak") ).get_parameter_value().string_value
        self.emote_dict = {
    "neutral":{
        "sound":"gbaby_quick_suprise.wav",
        "animation": self.animation_neutral,
        },
    "happy":{
        "sound":"gbaby_giggle.wav",
        "animation": self.animation_happy
        },
    "sad":{
        "sound":"gbaby_wakeup.wav",
        "animation": self.animation_sad
        },
    "close":{
        "sound":"gbaby_quick_suprise_5.wav",
        "animation": self.animation_close
        },
    "angry":{
        "sound":"gbaby_yummy.wav",
        "animation": self.animation_angry
        },
    "confused":{
        "sound":"gbaby_haah.wav",
        "animation": self.animation_confused
        },
    "suspicious":{
        "sound":"gbaby_quick_suprise_2.wav",
        "animation": self.animation_suspicious
        },
    "pain":{
        "sound":"gbaby_wakeup.wav",
        "animation": self.animation_pain
        },
    "unamused":{
        "sound":"gbaby_hay.wav",
        "animation": self.animation_unamused
        },
    "unsure":{
        "sound":"gbaby_he.wav",
        "animation": self.animation_unsure
        },
    "charger_connected":{
        "sound":"charger_connected.wav",
        "animation": self.animation_unsure
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
        self.create_subscription(String, '/xparo/response', self.speak_now, 10)
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

    def speak_now(self, message):
        text = str(message.data)
        self.get_logger().error(f"speak now is called {text}")
        try:
            dta = json.loads(text)
            text = dta["xparo"]
            ###############
            qq = String()
            qq.data = json.dumps({"emotion":self.detect_emotion(text)})
            self.xparo_send.publish(qq)
        except:
            pass
        threading.Thread(target =self.speak, args=(text,)).start()


    def stop_existing_playback(self):
        try:
            subprocess.run(['pkill', '-f', 'aplay'], check=True)
        except subprocess.CalledProcessError:
            pass


    def play_audio(self,file_path=None):
        if file_path is None:
            file_path = os.path.join(self.base_path,"tts_adjusted.wav")
        
        device_info = sd.query_devices(kind='output')
        print(f"Available output devices: {device_info}")
        sound = AudioSegment.from_file(file_path)
        play(sound)

        
    ############################################################
    ############################################################
    ############################################################

    def detect_emotion(self, text):
        # Normalize the text to lower case to improve matching
        text = str(text).lower()
        # Check each emotion pattern and find a match
        for emotion, pattern in self.emotion_patterns.items():
            if pattern.search(text):
                return emotion  # Return the first matching emotion
        return "none"  # Default to neutral if no emotion is detected

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


    def send_command(self, enable, pwm1, pwm2, pwm3, pwm4):
        command = f"{enable},{pwm1},{pwm2},{pwm3},{pwm4}\n"
        if self.arduino.is_open:
            self.arduino.write(command.encode("utf-8"))
            # time.sleep(0.02)


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
    def smooth_transition(self, start, end, duration):
        """
        Performs a smooth transition between start and end PWM values for all pins.
        """
        steps = 50
        delay_time = duration / steps
        for i in range(steps + 1):
            pwm1 = int(start[0] + (end[0] - start[0]) * i / steps)
            pwm2 = int(start[1] + (end[1] - start[1]) * i / steps)
            pwm3 = int(start[2] + (end[2] - start[2]) * i / steps)
            pwm4 = int(start[3] + (end[3] - start[3]) * i / steps)
            self.send_command(1, pwm1, pwm2, pwm3, pwm4)
            time.sleep(delay_time / 1000)

    def play_animation(self, emotion):
        """
        Plays the animation corresponding to the given emotion.
        """
        if self.running or emotion not in self.emote_dict:
            return

        animation_func = self.emote_dict[emotion]["animation"]
        sound_file = self.emote_dict[emotion]["sound"]
        self.play_audio(os.path.join(base_path_for_package,sound_file))

        self.running = True
        duration = random.randint(*self.animation_duration)
        print(f"Playing '{emotion}' animation with sound {sound_file} for {duration} seconds.")
        animation_thread = threading.Thread(target=animation_func, args=(duration,))
        animation_thread.start()
        animation_thread.join()
        self.running = False

        # Turn off lights after animation
        self.send_command(0, 0, 0, 0, 0)

    # Emotion Animations
    def animation_neutral(self, duration):
        """A steady, calm breathing pattern."""
        for _ in range(int(duration * 2)):
            self.smooth_transition((0, 128, 128, 0), (128, 0, 0, 128), 1000)
            self.smooth_transition((128, 0, 0, 128), (0, 128, 128, 0), 1000)

    def animation_happy(self, duration):
        """A bright and cheerful alternating flash."""
        for _ in range(int(duration * 5)):
            self.send_command(1, 255, 128, 0, 255)
            time.sleep(0.2)
            self.send_command(1, 0, 255, 128, 0)
            time.sleep(0.2)

    def animation_sad(self, duration):
        """A slow fade-out and fade-in with dim lighting."""
        for _ in range(int(duration * 2)):
            self.smooth_transition((0, 64, 64, 0), (0, 0, 0, 0), 1000)
            self.smooth_transition((0, 0, 0, 0), (0, 64, 64, 0), 1000)

    def animation_close(self, duration):
        """Both lights gradually fade to off."""
        for _ in range(int(duration)):
            self.smooth_transition((255, 255, 255, 255), (0, 0, 0, 0), 2000)

    def animation_angry(self, duration):
        """Fast, intense red flashes."""
        for _ in range(int(duration * 3)):
            self.send_command(1, 255, 0, 0, 0)
            time.sleep(0.1)
            self.send_command(1, 128, 0, 0, 64)
            time.sleep(0.1)

    def animation_confused(self, duration):
        """Alternating slow waves of blue and green."""
        for _ in range(int(duration * 4)):
            self.smooth_transition((0, 0, 255, 0), (0, 255, 0, 255), 1000)
            self.smooth_transition((0, 255, 0, 255), (0, 0, 255, 0), 1000)

    def animation_suspicious(self, duration):
        """Sharp pulses of red and dim blue."""
        for _ in range(int(duration * 5)):
            self.send_command(1, 255, 0, 64, 0)
            time.sleep(0.15)
            self.send_command(1, 128, 0, 32, 0)
            time.sleep(0.15)

    def animation_pain(self, duration):
        """Rapid jittery flashes."""
        for _ in range(int(duration * 10)):
            pwm1 = random.randint(128, 255)
            pwm2 = random.randint(0, 128)
            pwm3 = random.randint(128, 255)
            pwm4 = random.randint(0, 128)
            self.send_command(1, pwm1, pwm2, pwm3, pwm4)
            time.sleep(0.1)

    def animation_unamused(self, duration):
        """A slow, dull pulsating pattern."""
        for _ in range(int(duration * 2)):
            self.smooth_transition((64, 32, 32, 64), (0, 0, 0, 0), 1500)
            self.smooth_transition((0, 0, 0, 0), (64, 32, 32, 64), 1500)

    def animation_unsure(self, duration):
        """Erratic, alternating pulses."""
        for _ in range(int(duration * 5)):
            self.send_command(1, 128, 64, 128, 64)
            time.sleep(0.2)
            self.send_command(1, 64, 128, 64, 128)
            time.sleep(0.2)

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
