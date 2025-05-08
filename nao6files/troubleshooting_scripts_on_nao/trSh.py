from naoqi import ALProxy
import qi
import time

session = qi.Session()
session.connect("tcp://nao.local:9559")

# Update with your NAO's IP address and port
ROBOT_IP = "149.161.65.228"
ROBOT_PORT = 9559

def test_servos():
    diagnosis = session.service("ALDiagnosis")

    diagnosis_info = diagnosis.getActiveDiagnosis()

    print("Diagnosis:  ", diagnosis_info)

test_servos()
