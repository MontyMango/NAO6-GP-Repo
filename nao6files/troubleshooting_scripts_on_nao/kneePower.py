from naoqi import ALProxy
import qi
import time

ROBOT_IP="149.161.65.228"
ROBOT_PT=9559

def move_and_monitor_knees():
    # Create proxies
    #motion = ALProxy("ALMotion", ROBOT_IP, ROBOT_PT)
    memory = ALProxy("ALMemory", ROBOT_IP, ROBOT_PT)

    # Wake up the robot
    #motion.wakeUp()

    # Define joint names
    #knees = ["LKneePitch", "RKneePitch"]

    # Define target angles (in radians)
    # Example: bend knees slightly
    #target_angles = [0.5, 0.5]  # 0.5 rad = 28 degrees
    #speed_fraction = 0.2  # 20% of maximum speed

    #print("Starting knee movement...")
    #motion.setAngles(knees, target_angles, speed_fraction)

    # Start sampling currents
    start_time = time.time()
    #duration = 50  # seconds
    sample_interval = 0.1  # seconds

    print("Monitoring electric current during movement...")
    
    while time.time() - start_time > 0:
        l_current = memory.getData("Device/SubDeviceList/LKneePitch/ElectricCurrent/Sensor/Value")
        r_current = memory.getData("Device/SubDeviceList/RKneePitch/ElectricCurrent/Sensor/Value")
        
        print("Time: %.2fs | L Knee Current: %.3f A | R Knee Current: %.3f A" % (time.time() - start_time, l_current, r_current))

        time.sleep(sample_interval)

    print("Finished monitoring.")

    # Return to original posture
    #motion.rest()

if __name__ == "__main__":
    move_and_monitor_knees()
