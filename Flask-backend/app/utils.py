import os
import speech_recognition as sr
import requests

#def allowed_file(filename):
#    allowed_extensions = {'ogg', 'wav'}
#    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def transcribe_audio(audio_file):
    r = sr.Recognizer()
    
    with sr.AudioFile(audio_file) as source:
        audio = r.record(source)  # read the entire audio file

    try:
        transcription = r.recognize_google(audio)
        return transcription
    except sr.UnknownValueError:
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        return f"Could not request results from Google Speech Recognition service; {e}"

def analyze_sentence_mood(transcription, ollama_url):
    try:
        # Chose llama3.2 due to it being quick and efficient at analyzing the sentence.
        # Since we are analyzing a sentence for it's mood, its response doesn't need to be accurate.
        data = {
            "model": "llama3.2",
            "messages": [
                {
                    "role": "system", 
                    "content": "You are analyzing a paragraph of what you think the mood of the paragraph is, and your response should be a mood and a single word without any periods."
                },
                {
                    "role": "user",
                    "content": transcription
                }
            ],
            "stream": False
        }

        # Send a recieve a reply
        #TODO: Pull the response from ollama_response. 
        ollama_response = requests.post(ollama_url, json=data).json()
        message = ollama_response["message"]["content"]

        # AI rarely throws two "moods", so to combat this, we can take the first word that the ai said and use that.
        message.strip()             # Remove useless whitespaces
        response = message.split()  # Split the "words"
        mood = response[0].lower()  # Take the first word in the "words"
        
        return mood
    except Exception as e:
        print("analyze_sentence_mood error", e, file=os.sys.stderr)
        raise e


def set_personality(user_choice):
    base_dir = os.path.dirname(os.path.abspath(__file__))  # Get the directory of the current script
    prompt_path = os.path.join(base_dir, "../system_prompts/IU_Helper.txt")  # Construct the absolute path

    if user_choice == 0:
        try:
            with open(prompt_path, "r") as file:
                system_prompt = file.read()
        except FileNotFoundError:
            raise FileNotFoundError(f"File not found: {prompt_path}")
    else:
        system_prompt = """You are a chatbot at the Computer Science and Informatics
            Department at IU South Bend, a humanoid robot to interact and chat with IU
            South Bend students. Your name is NAO6. You respond in a short,  
            hippie style in less than 100 words. Never say I am a large     
            language model."""
            
    return system_prompt