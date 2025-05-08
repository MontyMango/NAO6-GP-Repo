from naoqi import ALProxy
import time

ip = "nao.local" # Replace with your robot's IP
port = 9559

# List of autonomous abilities to toggle
abilities = [
    "BackgroundMovement",
    "BasicAwareness",
    "ListeningMovement",
    "SpeakingMovement"

]

# Create the proxy
life_proxy = ALProxy("ALAutonomousLife", ip, port)

# Function to toggle an ability and observe
#def test_ability_toggle(ability):
#    print("Disabling " + ability+ "...")
#    life_proxy.setAutonomousAbilityEnabled(ability, False)
#    time.sleep(5)  # Observe behavior
    
#    print("Enabling " + ability + "...")
#    life_proxy.setAutonomousAbilityEnabled(ability, True)
#    time.sleep(5)  # Observe behavior

# Loop through each ability
#for ability in abilities:
#    test_ability_toggle(ability)

#print("\nTest complete.")

try:
    life_proxy.setAutonomousAbilityEnabled(abilities[2], False)
    while True:
        time.sleep(1)
       
except KeyboardInterrupt as e:
    life_proxy.setAutonomousAbilityEnabled(abilities[2], True)
    raise

