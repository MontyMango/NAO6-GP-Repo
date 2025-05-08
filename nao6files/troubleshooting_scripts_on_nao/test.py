from naoqi import ALProxy
import qi
import time

# Update with your NAO's IP address and port
ROBOT_IP = "149.161.65.228"
ROBOT_PORT = 9559

def test_servos():
    try:
        motion_proxy = ALProxy("ALMotion", ROBOT_IP, ROBOT_PORT)
    except Exception as e:
        print("Could not create proxy to ALMotion")
        print("Error was:", e)
        return

    # Wake up robot
    print("Waking up robot...")
    motion_proxy.wakeUp()

    session = qi.Session()
    session.connect("tcp://149.161.65.228:9559")

    diagnosis = session.service("ALDiagnosis")

    # Get the list of joints (you can specify manually if needed)
    joints = [
        "LShoulderPitch", "LShoulderRoll", "LElbowYaw", "LElbowRoll",
        "RShoulderPitch", "RShoulderRoll", "RElbowYaw", "RElbowRoll",
        "LHipYawPitch", "LHipRoll", "LHipPitch", "LKneePitch", "LAnklePitch", "LAnkleRoll",
        "RHipYawPitch", "RHipRoll", "RHipPitch", "RKneePitch", "RAnklePitch", "RAnkleRoll",
        "HeadYaw", "HeadPitch"
    ]

    # Move each joint a small amount to test
    for joint in joints:
        print("Testing ", joint, "...")
        current_angle = motion_proxy.getAngles(joint, True)[0]

        # Move 10 degrees up and down
        target_angle = current_angle + 0.17  # about 10 degrees
        motion_proxy.setAngles(joint, target_angle, 0.2)  # 0.2 is the speed (slow)
        time.sleep(1)
        
        target_angle = current_angle - 0.17
        motion_proxy.setAngles(joint, target_angle, 0.2)
        time.sleep(1)
        
        # Return to original position
        motion_proxy.setAngles(joint, current_angle, 0.2)
        time.sleep(1)

        diagnosis_info = diagnosis.getActiveDiagnosis()

        print("Diagnosis:  ", {diagnosis_info})

    # After testing
    print("Servos tested. Setting robot to rest...")
    motion_proxy.rest()

if __name__ == "__main__":
    test_servos()

