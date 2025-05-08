# -*- encoding: UTF-8 -*-

import sys
import time
from naoqi import ALProxy
import almath

def main(robotIP):
    PORT = 9559

    try:
        motionProxy = ALProxy("ALMotion", robotIP, PORT)
    except Exception, e:
        print "Could not create proxy to ALMotion"
        print "Error was: ", e
        sys.exit(1)

    # Set stiffness ON for both legs
    motionProxy.setStiffnesses(["LKneePitch", "RKneePitch"], 1.0)

    time.sleep(0.5)

    # Bend the knees slightly (~10 degrees)

    i=0
    while (i<10):
        names = ["LKneePitch", "RKneePitch"]
        angleLists = [20.0 * almath.TO_RAD, 20.0 * almath.TO_RAD]  # 10 degrees
        timeLists = [2.5, 2.5]  # move in 1.5 seconds
        isAbsolute = True
        print "Bending knees slightly..."
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

        time.sleep(1.0)

        # Return knees back to straight (0.0 rad)
        angleLists = [0.0, 0.0]
        timeLists = [1.5, 1.5]

        print "Returning knees to straight..."
        motionProxy.angleInterpolation(names, angleLists, timeLists, isAbsolute)

        time.sleep(1.0)
        i=i+1

    # Set stiffness OFF after test (optional)
    motionProxy.setStiffnesses(["LKneePitch", "RKneePitch"], 0.0)

    print "Knee bending test complete."

if __name__ == "__main__":
    robotIp = "nao.local"

    if len(sys.argv) <= 1:
        print "Usage: python almotion_angleinterpolation_knee.py robotIP (optional default: 127.0.0.1)"
    else:
        robotIp = sys.argv[1]

    main(robotIp)
