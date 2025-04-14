from flask import Blueprint, request, jsonify, Response
from app.utils import allowed_file, transcribe_audio
import requests

api = Blueprint('api', __name__)
OLLAMA_URL = "http://10.0.60.2:11434/api"
DATABASE_URL = "http://10.0.61.2:3306/"
global_AI_model = "qwen2.5:0.5b"    # Default can be something else
previous_transcription = ""
previous_response = ""
mood = "Netural"

# Use this to do a 
# moods = {
#     'Happy': '',
#     'Netural': '',
# }

# Procedure for robot
# 1. Set llm (Optional)
# 2. Download llm
# 3. Chat with llm


# https://stackabuse.com/step-by-step-guide-to-file-upload-with-flask/
@api.route('/transcribe', methods=['POST'])
def transcribe():
    # Check if a file is included in the request
    if 'file' not in request.files:
        return jsonify({"error": "No file attached!"}), 400
    file = request.files['file']

    # Validate the file format
    if file and allowed_file(file.filename):
        try:
            # Process the transcription
            transcription = transcribe_audio(file)
        except Exception as e:
            return jsonify({"error": str(e)}), 500

        # Return the transcription as a JSON response
        return jsonify({"transcription": transcription}), 200

    return jsonify({"error": "Invalid file format! Only .ogg and .wav files are allowed."}), 400


@api.route('/downloaded', methods=['GET'])
def get_models():
    response = requests.get(f"{OLLAMA_URL}/tags")
    return jsonify(response.json()), 200


@api.route('/running', methods=['GET'])
def get_running_models():
    response = requests.get(f"{OLLAMA_URL}/ps")
    return jsonify(response.json()), 200


# JSON Format:
# { model: 'modelName' }
@api.route('/download', methods=['POST'])
def download_model():
    data = request.json
    model = data.get("model", "")
    if not model:
        return jsonify({"error": "Model name is required"}), 400
    # Python streamed response: https://stackoverflow.com/questions/39272072/flask-send-stream-as-response#39274008
    response = requests.post(f"{OLLAMA_URL}/pull", json=data, stream=True)
    return Response(response.iter_content(chunk_size=10*1024)), 200


# JSON FORMAT:
# { model }
# TODO: We need to see how we can accept audio files through Flask.
@api.route('/chat', methods=['POST'])
def chat():
    try:
        # Check if an audio file is included in the request
        # If there isn't a file in the request, use the text
        if "file" not in request.files:
            transcription = request.json.prompt
        
        # Use the audio file instead (This take a little longer since we are using Google's transcription service)
        else:
            file = request.files['file']
            # Validate and transcribe the audio file
            if file and allowed_file(file.filename):
                try:
                    transcription = transcribe_audio(file)

                    # Make transcription available when getting the transcription
                    global previous_transcription
                    previous_transcription = transcription
                except Exception as e:
                    return jsonify({"error": f"Error during transcription: {str(e)}"}), 500
            else:
                return jsonify({"error": "Invalid file format! Only .ogg and .wav files are allowed."}), 400

        # Build the JSON request for the chat model
        data = request.json or {}
        data["messages"] = [{"role": "user", "content": transcription}]
        data["model"] = global_AI_model

        # Send the transcription to the chat model
        try:
            response = requests.post(f"{OLLAMA_URL}/chat", json=data)
            
            global previous_response
            previous_response = response.json().message.content
            return jsonify(response.json()), 200
        except Exception as e:
            return jsonify({"error": f"Error during chat request: {str(e)}"}), 500
    except Exception as e:
        return jsonify({"error": f"{e}"})


@api.route('/transcription', methods=['GET'])
def get_transcription():
    return jsonify({"transcription": previous_transcription})

@api.route('/response', methods=['GET'])
def get_response():
    return jsonify({"transcription": previous_response})

@api.route('/unload', methods=['POST'])
def unload_model():
    data = request.json
    data.messages = []
    data.keep_alive = 0

    response = requests.post(f"{OLLAMA_URL}/chat", json=data)
    return jsonify(response.json()), 200


@api.route('/show', methods=['POST'])
def get_model_information():
    data = request.json
    response = requests.post(f"{OLLAMA_URL}/show", json=data)
    return jsonify(response.json()), 200


@api.route('/delete', methods=['DELETE'])
def delete_model():
    data = request.json
    response = requests.delete(f"{OLLAMA_URL}/delete", json=data)
    return jsonify(response.json()), 200


@api.route('/set_llm', methods=['POST'])
def set_llm():
    # If the llm isn't filled, this might be called through a request. 
    data = request.json
    llm = data.get("model", "")
    if not llm:
        return jsonify({"error": "Model name is required"}), 400

    global global_AI_model
    global_AI_model = llm
    return jsonify({"message": f"Global AI model set to {llm}"}), 200

# FOR LONG STRETCH PROJECT
# @api.route('/describe-image', methods=['POST'])
# def chat_with_images():
#     data = request.json
#     response = request.post(f"{OLLAMA_URL}/chat", json=data)
#     return jsonify(response.json())