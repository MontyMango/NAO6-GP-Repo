import random
import subprocess

# Generate a random number between 1 and 22
num = random.randint(1, 22)

# Build the command string
cmd = 'qicli call ALAnimationPlayer.run "animations/Stand/BodyTalk/Speaking/BodyTalk_{}"'.format(num)

# Execute the command
subprocess.call(cmd, shell=True)

