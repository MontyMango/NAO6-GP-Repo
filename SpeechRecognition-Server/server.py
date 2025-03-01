import socket
import speech_recognition as sr
from os import path

PORT_NUMBER = 45689
AUDIO_FILE_NAME = "audioFile.ogg"

def receive_file(server_ip, server_port, output_file):
    # Create a TCP/IP socket
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Bind the socket to the server address and port
    server_socket.bind((server_ip, server_port))
    server_socket.listen(1)
    print("Server listening...")

    # Wait for a connection
    connection, client_address = server_socket.accept()
    print("Connection established with "+str(client_address))

    with open(output_file, 'wb') as f:
        print("Receiving file and saving as "+str(output_file))
        while True:
            # Receive data in small chunks
            data = connection.recv(1024)
            if not data:
                break
            f.write(data)

    print("File received successfully.")
    connection.close()

def transcribeAudio(audioFileName):
    # get the path of the file 
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), audioFileName)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition, using Google's default API key
    try:
        print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

#
while __name__ == '__main__':
    receive_file("0.0.0.0", PORT_NUMBER, AUDIO_FILE_NAME)
    transcribeAudio(AUDIO_FILE_NAME)
    # Need to send back transcribed audio though.