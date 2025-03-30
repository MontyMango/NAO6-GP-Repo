from flask import Blueprint, request, jsonify, Response
from werkzeug.utils import secure_filename
from app.utils import allowed_file, transcribe_audio
import requests

api = Blueprint('api', __name__)
OLLAMA_URL = "http://10.0.60.2:11434/api"
DATABASE_URL = "http://10.0.61.2:3306/"

# https://stackabuse.com/step-by-step-guide-to-file-upload-with-flask/
@api.route('/transcribe', methods=['POST'])
def transcribe():
    if 'file' not in request.files:
        return jsonify({"error": "No file attached!"}), 400
    
    file = request.files['file']
    
    if file and allowed_file(file.filename):
        try:
            filename = secure_filename(file.filename)
            transcription = transcribe_audio(file)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
        return jsonify({"transcription": transcription}), 200
    
    return jsonify({"error": "Invalid file format! Only .ogg and .wav files are allowed."}), 400


@api.route('/downloaded', methods=['GET'])
def get_models():
    response = requests.get(f"{OLLAMA_URL}/tags")
    return jsonify(response.json())


@api.route('/running', methods=['GET'])
def get_running_models():
    response = requests.get(f"{OLLAMA_URL}/ps")
    return jsonify(response.json())


# JSON Format:
# { model: 'modelName' }
@api.route('/download', methods=['POST'])
def download_model():
    data = request.json
    # Python streamed response: https://stackoverflow.com/questions/39272072/flask-send-stream-as-response#39274008
    response = requests.post(f"{OLLAMA_URL}/pull", json=data, stream=True)
    return Response(response.iter_content(chunk_size=10*1024))

# JSON FORMAT:
# { model }
# TODO: We need to see how we can accept audio files through Flask.
@api.route('/chat', methods=['POST'])
def chat():
    # 1. Process audio first and transcribe the audio
    if "file" not in request.files:
        return jsonify({"error": "No file uploaded"}), 400

    file = request.files['file']
    transcription = transcribe_audio(file)

    # 2. Build the JSON request
    data = request.json
    data.messages.role = "user"

    # USE IF YOU WANT TO PROMPT ENGINEER
    # data.messages.content +=

    response = requests.post(f"{OLLAMA_URL}/chat", json=data)
    return jsonify(response.json())


@api.route('/unload', methods=['POST'])
def unload_model():
    data = request.json
    data.messages = []
    data.keep_alive = 0

    response = requests.post(f"{OLLAMA_URL}/chat", json=data)
    return jsonify(response.json())


@api.route('/show', methods=['POST'])
def get_model_information():
    data = request.json
    response = requests.post(f"{OLLAMA_URL}/show", json=data)
    return jsonify(response.json())


@api.route('/delete', methods=['DELETE'])
def delete_model():
    data = request.json
    response = requests.delete(f"{OLLAMA_URL}/delete", json=data)
    return jsonify(response.json())


# FOR LONG STRETCH PROJECT
# @api.route('/describe-image', methods=['POST'])
# def chat_with_images():
#     data = request.json
#     response = request.post(f"{OLLAMA_URL}/chat", json=data)
#     return jsonify(response.json())