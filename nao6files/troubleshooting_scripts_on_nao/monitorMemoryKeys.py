#!/usr/bin/python

from naoqi import ALProxy
import datetime
import time

memory = ALProxy("ALMemory", "nao.local", 9559)

while 1:
    waveDet = memory.getData("Launchpad/WavingDetection")
    peopSee = memory.getData("Launchpad/PeopleNotSeen")
    currAct = memory.getData("Launchpad/FocusedActivity")
    prevAct = memory.getData("Launchpad/PreviousActivity")
    dt = datetime.datetime.fromtimestamp(time.time())
    now = dt.strftime('%H:%M:%S')
    #print("Time: %.2fs | Current: %s | Previous: %s | Seen: %s | Wave: %s" % (time.time(), currAct, prevAct, peopSee, waveDet))
    print("Time: %s | Current: %s | Previous: %s | NOTSeen: %s | Wave: %s" % (now, currAct, prevAct, peopSee, waveDet))
    time.sleep(1)

