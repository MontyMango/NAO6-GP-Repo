import qi
import time

def main(robot_ip="127.0.0.1", port=9559):
    session = qi.Session()
    try:
        session.connect("tcp://149.161.65.228:9559")
    except RuntimeError:
        print("Can't connect to Naoqi at 149.161.65.228:9559")
        return

    memory = session.service("ALMemory")

    # List of the joints you want
    #joints = ["LKneePitch", "RKneePitch"]

    # Get the list of joints (you can specify manually if needed)
    joints = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll",
        "HeadYaw", "HeadPitch"
    ]

    try: 
        while True:
            for joint in joints:
                print "--- Data for ", joint, " ---"
                # List all keys that match this joint
                keys = memory.getDataListName()
                joint_keys = [k for k in keys if joint in k]
                for key in joint_keys:
                    try:
                        value = memory.getData(key)
                        print key, " = ", value
                    except Exception as e:
                        print "Could not read ", key, ":", e
            time.sleep(0.5)  # update every half second
    except KeyboardInterrupt:
        print("\nStopped monitoring.")

if __name__ == "__main__":
    main(robot_ip="149.161.65.228")  # Replace with your robot IP

