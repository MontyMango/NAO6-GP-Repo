#!/bin/python

from naoqi import ALProxy, ALModule
import qi
import time
import subprocess
import sys
import threading

class HeadTouchStart:
    def __init__(self, session):
        self.memory = session.service("ALMemory")
        self.subscriber = self.memory.subscriber("RearTactilTouched")
        self.tts = session.service("ALTextToSpeech")
        self.signal_id = self.subscriber.signal.connect(self.on_head_touched)

    def on_head_touched(self, value):
        #try: 
        if value == 1.0:
            self.tts.say("Hey, are you scratching me?")
            print("Rear of head touched!")

            # Unsubscribe to prevent repeated triggers
            self.subscriber.signal.disconnect(self.signal_id)

            thread = threading.Thread(target=self.run_script_and_resubscribe)
            thread.start()

            self.signal_id = self.subscriber.signal.connect(self.on_head_touched)
            print("Re-subscribed to RearTactilTouched")

        #except Exception as e:
        #    print("Value error caught in function: " + e)

    def run_script_and_resubscribe(self):
        try:
            # Run your custom script and wait for it to finish
            process = subprocess.Popen(["python", "/home/nao/scripts/record-and-respond_NO-Knees.py"])
            process.wait()

        except Exception as e:
            print("Error running script:", e)

        # Re-subscribe to the touch event
        self.signal_id = self.subscriber.signal.connect(self.on_head_touched)
        print("Re-subscribed to RearTactilTouched")

def main():
    # Connect to NAOqi session
    try:
        connection_url = "tcp://nao.local:9559"  # Replace with your robot's IP if remote
        app = qi.Application(["HeadTouchStart", "--qi-url=" + connection_url])
        app.start()
        session = app.session
    except RuntimeError:
        print("Can't connect to Naoqi")
        sys.exit(1)

    head_touch_start = HeadTouchStart(session)
    try:
        while True:
            print("Running... (press rear head sensor to start your program)")
            time.sleep(2)
    except KeyboardInterrupt:
        print("Interrupted by user, shutting down.")

if __name__ == "__main__":
    main()

