from flask import Blueprint, request, jsonify
from app.utils import transcribe_audio, analyze_sentence_mood, set_personality
import requests
import os

api = Blueprint('api', __name__)

# URLS
OLLAMA_URL = "http://10.0.68.2:11434/api"
# DATABASE_URL = "http://10.0.68.3:3306/"

# GLOBAL VARIABLES
global_AI_model = "qwen2.5:0.5b"    # Default can be something else
global_mood = "neutral"

# Used for displaying what mood NAO6 is in for the website
placeholder_mood = global_mood

# TRANSCRIPTIONS USED 
previous_transcription = "Whatever NAO6 thought you said will show up here"
previous_response = "NAO6's response will show up here"

# Prompt engineering for moods
reg_system_prompt = set_personality(0)
snarky_system_prompt = set_personality(1)

# Procedure for robot
# 1. Set llm (Optional)
# 2. Download llm
# 3. Chat with llm

# https://stackabuse.com/step-by-step-guide-to-file-upload-with-flask/
@api.route('/transcribe', methods=['POST'])
def transcribe():
    try:
        # Check if a file is included in the request
        if 'file' not in request.files:
            return jsonify({"error": "No file attached!"}), 400
        file = request.files['file']

        # Validate the file format
        try:
            # Process the transcription
            transcription = transcribe_audio(file)
        except Exception as e:
            return jsonify({"Transcription error": str(e)}), 500

        # Return the transcription as a JSON response
        return jsonify({"transcription": transcription}), 200
    except:
        return jsonify({"Transcribe error": "Invalid file format! Only .ogg and .wav files are allowed."}), 400


@api.route('/downloaded', methods=['GET'])
def get_models():
    response = requests.get(f"{OLLAMA_URL}/tags")
    return jsonify(response.json()), 200


# @api.route('/running', methods=['GET'])
# def get_running_models():
#     response = requests.get(f"{OLLAMA_URL}/ps")
#     return jsonify(response.json()), 200


# Downloading isn't required since every model will be downloaded beforehand.
# JSON Format:
# { model: 'modelName' }
# @api.route('/download', methods=['POST'])
# def download_model():
#     data = request.json
#     model = data.get("model", "")
#     if not model:
#         return jsonify({"error": "Model name is required"}), 400
#     # Python streamed response: https://stackoverflow.com/questions/39272072/flask-send-stream-as-response#39274008
#     response = requests.post(f"{OLLAMA_URL}/pull", json=data, stream=True)
#     return Response(response.iter_content(chunk_size=10*1024)), 200


# JSON FORMAT:
# { model }
@api.route('/chat', methods=['POST'])
def chat():
    try:
        if "file" not in request.files:
            return jsonify({"error": "No file uploaded"}), 400
        
        file = request.files["file"]
        file_path = f"/temp/{file.filename}"
        file.save(file_path)
        # print("File saved!", file_path, file=os.sys.stderr)

        transcribed_text = transcribe_audio(file_path)
        os.remove(file_path)  # Cleanup

        # Make transcription available when getting the transcription
        global previous_transcription
        previous_transcription = transcribed_text

        # Mood prompt engineering
        chat_url = OLLAMA_URL + "/chat"

        # Get the mood
        if global_mood == 'dynamic':
            mood = analyze_sentence_mood(transcribed_text, chat_url)

            global placeholder_mood
            placeholder_mood = mood
        else:
            mood = global_mood
        print("Mood:", mood, file=os.sys.stderr)

        # Constructing the system prompt
        if mood == "neutral":
            sysPrompt = reg_system_prompt
        elif mood == "sassy":
            sysPrompt = snarky_system_prompt
        else:
            sysPrompt = reg_system_prompt+"Your mood is " +mood
        print("System prompt", sysPrompt, file=os.sys.stderr)

        # Send transcribed text to Ollama
        data = {
            "model": global_AI_model,
            "messages": [
                {
                    "role": "system",
                    "content": sysPrompt
                },
                {
                "role": "user",
                "content": transcribed_text
                }
            ],
            "stream": False
        }
        print("data", data, file=os.sys.stderr)

        # Send a recieve a reply
        ollama_response = requests.post(chat_url, json=data)
        # Parse and print the response
        if ollama_response.status_code == 200:
            reply = ollama_response.json()

            # Set as a the previous response so it can show up on the website
            global previous_response
            previous_response = reply["message"]["content"]
            print(reply)
            
            print("Model reply:", reply["message"]["content"])
            response = jsonify({"transcribed_text": transcribed_text,
                            "ollama_response": reply["message"]["content"]})
        else:
            print("Error:", response.status_code, response.text)
            response = jsonify({"transcribed_text": transcribed_text,
                            "ollama_response": response.text })
        return response
    
    except Exception as e:
        return jsonify({"chat() error":f"{e}"}), 400


@api.route('/transcription', methods=['GET'])
def get_transcription():
    return jsonify({"transcription": previous_transcription}), 200


@api.route('/response', methods=['GET'])
def get_response():
    return jsonify({"transcription": previous_response}), 200

# Since our React app has a
@api.route('/get_llm_and_mood')
def get_llm_and_mood():
    return jsonify({"mood": placeholder_mood, "llm": global_AI_model}), 200


# @api.route('/unload', methods=['POST'])
# def unload_model():
#     data = request.json
#     data.messages = []
#     data.keep_alive = 0

#     response = requests.post(f"{OLLAMA_URL}/chat", json=data)
#     return jsonify(response.json()), 200


# @api.route('/show', methods=['POST'])
# def get_model_information():
#     data = request.json
#     response = requests.post(f"{OLLAMA_URL}/show", json=data)
#     return jsonify(response.json()), 200


# @api.route('/delete', methods=['DELETE'])
# def delete_model():
#     data = request.json
#     response = requests.delete(f"{OLLAMA_URL}/delete", json=data)
#     return jsonify(response.json()), 200


@api.route('/set_llm', methods=['POST'])
def set_llm():
    # If the llm isn't filled, this might be called through a request. 
    data = request.json
    llm = data.get("model", "")
    if not llm:
        return jsonify({"message": "Model name is required"}), 400

    global global_AI_model
    global_AI_model = llm
    return jsonify({"message": f"Global AI model set to {llm}"}), 200


@api.route('/set_mood', methods=['POST'])
def set_mood():
    data = request.json
    mood = data.get("mood", "")

    if not mood:
        return jsonify({"message": "Mood statement is required"}), 400
    
    
    global placeholder_mood
    global global_mood
    global_mood = mood
    placeholder_mood = mood

    return jsonify({"message": f"Global mood is set to {mood}"}), 200
