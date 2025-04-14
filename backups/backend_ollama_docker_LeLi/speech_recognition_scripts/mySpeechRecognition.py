from flask import Flask, request, jsonify
import speech_recognition as sr
import requests
import os

app = Flask(__name__)

OLLAMA_URL = "http://localhost:11434/api/generate" 

def transcribe_audio(audio_path):
    #recognizer = sr.Recognizer()
    recognizer = sr.Recognizer()
    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)
    try: 
        text=recognizer.recognize_google(audio, show_all=True)
        best_transcript = max(text['alternative'], key=lambda x: x['confidence'])['transcript']

        return best_transcript 
    except sr.UnknownValueError:
        print("Google Speech Recognition could not understand audio")
        return "Google Speech Recognition could not understand audio"
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))
        return "Could not request results from service"

@app.route("/process", methods=["POST"])
def process_audio():
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400
    
    file = request.files["file"]
    file_path = f"temp/{file.filename}"
    file.save(file_path)

    #try:
    # Transcribe audio
    prompt = "You are a chatbot named nao6. For the following user prompt, create response of less than 200 words. The prompt is: "
    transcribed_text = transcribe_audio(file_path)
    os.remove(file_path)  # Cleanup

    # Send transcribed text to Ollama
    data = {
        "model": "deepseek-r1:7b",
        "prompt": prompt+transcribed_text,
        "stream": False
    }

    ollama_response = requests.post(OLLAMA_URL, json=data)
        
    return jsonify({"transcribed_text": transcribed_text, "ollama_response": ollama_response.json()})

    #except Exception as e:
    #    return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    os.makedirs("temp", exist_ok=True)
    app.run(host="0.0.0.0", port=45689)

