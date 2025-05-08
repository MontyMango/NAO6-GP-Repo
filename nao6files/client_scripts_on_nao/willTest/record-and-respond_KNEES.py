import qi
import sys
import json
import os
import time
import numpy as np
import requests
from naoqi import ALProxy

class HeadTouchException(Exception):
    pass

###################
# The Chatbot Class  
###################
class ChatBot:

###################
# Constructor.  
###################
    def __init__(self): 

        # Assigns robot ip and port.
        ip = "nao.local"  # NAO6's fully-qualified domain name
        port = 9559  # Default port

        # Assigns the server URL of the backend, and the path of user voice
        # recording.
        self.SERVER_URL = "http://149.161.65.104:45689/process"
        #self.SERVER_URL = "http://149.161.65.104:43016/chat"
        self.AUDIO_FILE = "/home/nao/scripts/tmp/test.ogg"

        # Start qi session to access ALAutonomousLife, ALMotion,
        # ALRobotPosture, ALAnimationPlayer, and ALMemory. 
        self.session = qi.Session()
        self.session.connect("tcp://nao.local:9559")

        # Set ALProxies for audio recording, eyes led control, and animated
	# speech.
        self.audio_device = ALProxy("ALAudioDevice", ip, port)
        self.leds = ALProxy("ALLeds", ip, port)
        self.lm = ALProxy("ALListeningMovement", ip, port)
        self.blinking_proxy = ALProxy("ALAutonomousBlinking", ip, port)
        #self.tts = ALProxy("ALAnimatedSpeech", ip, port)
        self.tts = ALProxy("ALTextToSpeech", ip, port)
        self.video_proxy = ALProxy("ALVideoDevice", ip, port)

        # Set qi session services for autonomous life, animation, motion,
        # balance control, posture, etc. 
        self.autonomous_life = self.session.service("ALAutonomousLife")
        self.motion = self.session.service("ALMotion")
        self.posture = self.session.service("ALRobotPosture")
        self.player = self.session.service("ALAnimationPlayer")
        self.memory = self.session.service("ALMemory")

        # Set event subscriber to monitor FrontTactileTouched event.  
        self.subscriber = None
        self.signal_id = None
        self.head_touched = None

################
# Get NAO6 ready for chatbot script. This part includes disabling
# autonomous life, resetting balance, bringing the robot back to
# standing position, playing welcome message and animation, and
# subscribe to FrontTactilTouched event so that the user can touch the
# robot's head to stop the program later.  
################
    def set_initial_posture(self):
        #self.autonomous_life.setState("solitary")
        print("autonomous life set")
        time.sleep(1)
        #self.posture.goToPosture("SitRelax", 0.8)  # 0.8 is the speed (0.0 to 1.0)
        #self.autonomous_life.setState("disabled")
        self.lm.setEnabled(False)
        self.blinking_proxy.setEnabled(False) # Disable the eye blinking
        print("autonomous life set")

        self.motion.wbEnable(True)
        print("balance life set")
        self.motion.wakeUp()
        print("wake up set")
        #self.posture.goToPosture("SitRelax", 0.8)  # 0.8 is the speed (0.0 to 1.0)

        self.tts.say("Hi, I am Nao. Do you want to have a chat with me? I am listening when my eyes are blue. When my eyes are pink, I am thinking about my response. And my eyes are green when I am talking. To end the chat, just put your hand on my head.")

        self.player.run("animations/Stand/Gestures/Claw_2")

        # Unsubscribe all active clients (optional: if you know the client name, you can just unsubscribe that)
        try:
            # Get list of active subscriptions
            subscribers = self.video_proxy.getSubscribers()
            for name in subscribers:
                print(name)
                video_proxy.unsubscribe(name)
            print("Camera feed(s) unsubscribed.")
        except Exception as e:
            print("Error unsubscribing camera:", e)

        self.subscriber = self.memory.subscriber("FrontTactilTouched")
        self.signal_id = self.subscriber.signal.connect(self.on_head_touched)
        self.head_touched = 0
        print("[INFO] Press the front head sensor to stop the script.")

########################
# This function is triggered upon FrontTactilTouched event. It plays a
# message and sets the head_touched flag to 1. 
########################
    def on_head_touched(self, value):
        if value == 1.0:  # If the FrontTactil sensor returns 1.0.
            print("[INFO] Front head touch detected exiting.")
            self.tts.say("Hey, that tickles!")
            self.head_touched = 1

            # Unsubscribe after setting flag.
            self.subscriber.signal.disconnect(self.signal_id)

#######################
# This function is called by the record_audio function to check fori
# front microphone energy to enable adaptive recording.
#######################
    def get_sound_energy(self):

        # Get microphone energy level from ALAudioDevice.
        buffer = self.audio_device.getFrontMicEnergy()
        return np.mean(buffer) if buffer else 0

#######################
# This function is called in Main to wait for the sound level to
# exceed a minimum threashold, then begin recording and put audio in
# the self.AUDIO_FILE.
#######################
    def record_audio(self):

        # Time in seconds of silence before stopping recording
        silence_threshold = 2.0

        # Adjust based on testing (lower = more sensitive)
        energy_threshold = 1000

        # Adjust based on testing
        upper_energy_threshold = 9000

        try:
            # Start recording if the front microphone hears a sound within
            # thresholds.
            recording_file = self.AUDIO_FILE
            print("Listening for sounds...")

            # Set eye color to blue to indicate that NAO6 is listening.  
            self.leds.fadeRGB("FaceLeds", 0x0000FF, 1.0)

            while True:
                # Skip is head_touched flag is set.
                if self.head_touched == 1:
                    print("Head was touched. Skip recording.")
                    break
                sound_start_time=0
                energy = self.get_sound_energy()

                if (energy > energy_threshold and energy < upper_energy_threshold):
                    print("Sound detected! Energy: "+str(energy)+". Starting recording...")
                    self.audio_device.startMicrophonesRecording(recording_file)

                    # Play animation to indicate that recording has started.
                    self.player.run("animations/Stand/BodyTalk/BodyLanguage/NAO/Left_Neutral_AFF_02")
                    break
                time.sleep(0.2)

            # Monitor silence
            last_sound_time = time.time()
        
            while True:
                # Skip is head_touched flag is set.
                if self.head_touched == 1:
                    print("Head was touched. Stop recording and skip.")
                    self.audio_device.stopMicrophonesRecording()
                    break

                time.sleep(0.5)
                energy = self.get_sound_energy()
                print("Sound Energy: "+str(energy))

                # Reset timer if sound detected
                if energy > energy_threshold:  
                    last_sound_time = time.time()
        
                # Stop recording if silence exceeds threshold
                if time.time() - last_sound_time >= silence_threshold:
                    print("Silence detected. Stopping recording...")

                    # Set eyes to pink to indicate recording has stopped.
                    self.leds.fadeRGB("FaceLeds", 0xFF00FF, 1.0)
                    self.audio_device.stopMicrophonesRecording()

                    # Play thinking animation.
                    self.player.run("animations/Stand/BodyTalk/Thinking/Remember_3")
                    break

        except Exception as e:
            self.audio_device.stopMicrophonesRecording()
            print("An error occurred: "+str(e))

###################
# This reads an audio file from the "self.AUDIO_FILE" and sends it to the
# backend server for processing.  Then it receives the Ollama response and
# makes the robot speak it.
###################
    def send_audio(self):

        # Send an audio file from NAO6 to the remote server.
        try:
            # Skip IFF is head_touched flag is set.
            if self.head_touched == 1.0:
                print("Head was touched. Skip sending files.")
                return

            # Send recording self.AUDIO_FILE to the backend server
            # self.SERVER_URL and receive the server's response.  
            with open(self.AUDIO_FILE, "rb") as f:
                headers = {"X-API-KEY": "dbzgt123"}
                files = {"file": f}
                #response = requests.post(SERVER_URL, headers=headers, files=files, verify="./cs03Pub.crt")
                response = requests.post(self.SERVER_URL, headers=headers, files=files)

            # Print server response.
            print("Server Response:", response.text)
        
            # Skip if head_touched flag is set.
            if self.head_touched == 1.0:
                print("Head was touched. Skip talking.")
                return

            # Parse server response. If it is from OLLAMA, then parse the json
            # file. If it's not json, then just receive response.text field.
            try: 
                response_data = json.loads(response.text)
                #response_entry = response_data.get('ollama_response', {}).get('response', 'No response found') # Old format. The backend server used to return the full json from ollama response as a field. 
                response_entry = response_data.get('ollama_response', 'No response found') # Improved return json structure. Now the ollama_response field contains the LLM response text or error messages. 
                print("response_entry is ", response_entry)
            except Exception as e:
                print("no json file? "+str(e))
                response_entry = "An error occurred with receiving the response from the server." 

            # Set eye color to green to indicate the robot is ready to talk.
            # Read the OLLAMA response with ALAnimatedSay. 
            self.leds.fadeRGB("FaceLeds", 0x00FF00, 1.0)
            self.tts.say(str(response_entry))
            self.leds.fadeRGB("FaceLeds", 0xFFFFFF, 1.0)

        except Exception as e:
            print("Error sending file:", e)

################################
# In case of interrupt, stop microphone recording, play goodbye
# animation and message, and bring autonomous life state back to
# solitary.
################################
    def graceful_exit(self):
        self.audio_device.stopMicrophonesRecording()
        self.leds.fadeRGB("FaceLeds", 0xFFFFFF, 1.0)
        self.blinking_proxy.setEnabled(True)
        self.player.run("animations/Stand/Gestures/Wings_4")
        self.tts.say("Bye. See you next time.")
        self.player.run("animations/Stand/Emotions/Negative/Sad_1")
        time.sleep(2)
        #self.autonomous_life.setState("solitary")
        time.sleep(1)
        self.tts.say("Bye.")

################################
# main function 
#
# Declare an instance of the ChatBot class.
# Set the robot into chatbot posture.
################################
print("Script started")
nao_chatbot = ChatBot()
print("ChatBot instance generated")
nao_chatbot.set_initial_posture()

try:
    while True:

        # Record user message.
        nao_chatbot.record_audio()

        # Raise exception if head_touched flag is set to break out of the loop.
        if nao_chatbot.head_touched == 1:
            raise HeadTouchException("Head was touched!")

        # Send recorded audio file and play OLLAMA response.
        nao_chatbot.send_audio()
        time.sleep(0.5)

        # Raise exception if head_touched flag is set to break out of the loop.
        if nao_chatbot.head_touched == 1:
            raise HeadTouchException("Head was touched!")

        # Play animation to indicate that NAO6 is ready for another question.
        nao_chatbot.player.run("animations/Stand/Gestures/Thinking_1")

except KeyboardInterrupt:
    print("Program interrupted by user, stopping.")
    nao_chatbot.graceful_exit()

    # Re-raise the KeyboardInterrupt to stop the program
    raise

except HeadTouchException as e:
    print("Head was touched. Stop the program.") 
    nao_chatbot.tts.say("You touched my head. I guess I will be quiet.")
    nao_chatbot.graceful_exit()
    raise

except Exception as e:
    print("Error occurred: "+str(e)+". Skipping.")
    nao_chatbot.graceful_exit()
    raise






#def check_head_touch():
#    front = memory.getData("FrontTactilTouched")
#    middle = memory.getData("MiddleTactilTouched")
#    rear = memory.getData("RearTactilTouched")
#    if front == 1.0 or middle == 1.0 or rear == 1.0:
#        raise HeadTouchException("Head was touched!")


