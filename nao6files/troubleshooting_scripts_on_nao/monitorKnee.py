from naoqi import ALProxy
import qi
import time

# Change this to your robot's IP address
ROBOT_IP = "149.161.65.228"
PORT = 9559

# Create proxies
motion = ALProxy("ALMotion", ROBOT_IP, PORT)
session = qi.Session()

try:
    session.connect("tcp://nao.local:9559")
except RuntimeError:
    print("Can't connect to Naoqi at ", ROBOT_IP, ":", PORT)

# Get the DCM service
dcm = session.service("DCM")

# List of joints we want to monitor (knees)
knee_joints = ["LKneePitch", "RKneePitch"]

print("Starting Knee Joint Health Check...\n")

try:
    while True:
        angles = motion.getAngles(knee_joints, True)  # True = in absolute coordinates
        stiffnesses = motion.getStiffnesses(knee_joints)
        key = "Device/SubDeviceList/{knee_joints}"
        value = dcm.getData(key)
        print("Left knee angle is ", angles[0])
        print("Stiffness is ", stiffnesses[0])
        print("Left knee angle is ", angles[1])
        print("Stiffness is ", stiffnesses[1])
        print("-" * 40)
        #print("Hardness actuator value for {knee_joints}: ", {value})

        time.sleep(0.5)  # update every half second

except KeyboardInterrupt:
    print("\nStopped monitoring.")

