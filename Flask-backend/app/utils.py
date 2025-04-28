#def allowed_file(filename):
#    allowed_extensions = {'ogg', 'wav'}
#    return '.' in filename and filename.rsplit('.', 1)[1].lower() in allowed_extensions

def transcribe_audio(audio_file):
    import speech_recognition as sr
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
    import requests
    # Chose qwen2.5:0.5b for it's lightweight and quick responses.
    # Since we are analyzing a sentence for it's mood, its response doesn't need to be accurate.
    data = {
        "model": "qwen2.5:0.5b",
        "messages": [
            {
                "role": "system", 
                "content": "You are analyzing a sentence of what you think the mood of the sentence is, and your response should be a single word."
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
    message = ollama_response["message"]["content"]["text"]

    # AI rarely throws two "moods", so to combat this, we can take the first word that the ai said and use that.
    message.strip()             # Remove useless whitespaces
    response = message.split()  # Split the "words"
    mood = response[0].lower()  # Take the first word in the "words"
    
    return mood


def import_sys_prompt():
    return 