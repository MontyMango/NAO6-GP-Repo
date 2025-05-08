import qi
import sys
import json
import os
import time
import numpy as np
import requests
from naoqi import ALProxy

ip = "nao.local"  # NAO6's fully-qualified domain name
port = 9559  # Default port
audio_device = ALProxy("ALAudioDevice", ip, port)
tts = ALProxy("ALAnimatedSpeech", ip, port)

session = qi.Session()
session.connect("tcp://nao.local:9559")
memory = session.service("ALMemory")

def send_audio(file_path, tts):
    """Send an audio file from NAO6 to the remote server."""
    try:
        with open(file_path, "rb") as f:
            headers = {"X-API-KEY": "dbzgt123"}
            files = {"file": f}
            #response = requests.post(SERVER_URL, headers=headers, files=files, verify="./cs03Pub.crt")
            response = requests.post(SERVER_URL, headers=headers, files=files)

        print("Server Response:", response.text)
        #try: 
        #    response_data = json.loads(response.text)
        #    response_entry = response_data.get('ollama_response', {}).get('response', 'No response found')
        #    print("response_entry is ", response_entry)
        #except Exception as e:
        #    print("no json file? "+str(e))
        #    response_entry = response.text 
        #robot_ip = "nao.local"
        #port = 9559
        #tts.say(str(response_entry))
        return 0

    except Exception as e:
        print("Error sending file:", e)
        return 0

# Run the function

SERVER_URL = "http://149.161.65.104:43016/chat"
AUDIO_FILE = "/home/nao/scripts/tmp/test.ogg"
send_audio(AUDIO_FILE, tts)

