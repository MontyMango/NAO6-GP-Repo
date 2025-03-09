from flask import Blueprint, request, jsonify
from werkzeug.utils import secure_filename
from app.utils import allowed_file, transcribe_audio

api = Blueprint('api', __name__)

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