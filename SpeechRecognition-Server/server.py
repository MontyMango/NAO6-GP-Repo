import socket
import speech_recognition as sr
from os import path

# Changeable variables (That will not destroy the program!)
PORT_NUMBER = 45689
AUDIO_FILE_NAME = "audioFile.ogg"



# This is the main function for the audio transcription server
def mainFunction(server_ip, server_port, output_file):
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

        # Recieve the audio
        while True:
            data = connection.recv(1024)    # Receive data in small chunks
            if not data:
                break
            f.write(data)
        print("File received successfully.")

        # Transcribe the audio
        transcribedAudio = transcribeAudio(f)

        # Send the transcription back 
        connection.send(transcribeAudio)

    connection.close()



# This handles the transcribed audio
def transcribeAudio(audioFileName):
    # get the path of the file 
    AUDIO_FILE = path.join(path.dirname(path.realpath(__file__)), audioFileName)

    # use the audio file as the audio source
    r = sr.Recognizer()
    with sr.AudioFile(AUDIO_FILE) as source:
        audio = r.record(source)  # read the entire audio file

    # recognize speech using Google Speech Recognition, using Google's default API key
    audioTranscription = r.recognize_google(audio)
    try:
        print("Google Speech Recognition thinks you said " + audioTranscription)
        return audioTranscription
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))



# MAIN FUNCTION
while __name__ == '__main__':
    mainFunction("0.0.0.0", PORT_NUMBER, AUDIO_FILE_NAME)