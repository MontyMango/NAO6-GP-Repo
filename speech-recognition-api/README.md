# Speech Recognition API

This project is a Flask-based REST API that accepts audio files and transcribes them using the Speech Recognition library. It provides a simple interface for users to upload audio files and receive transcriptions in response.

## Project Structure

```
speech-recognition-api
├── app
│   ├── __init__.py
│   ├── routes.py
│   └── utils.py
├── requirements.txt
├── run.py
└── README.md
```

## Setup Instructions

1. **Clone the repository:**
   ```
   git clone <repository-url>
   cd speech-recognition-api
   ```

2. **Create a virtual environment:**
   ```
   python -m venv venv
   source venv/bin/activate  # On Windows use `venv\Scripts\activate`
   ```

3. **Install the required packages:**
   ```
   pip install -r requirements.txt
   ```

## Usage

1. **Run the application:**
   ```
   python run.py
   ```

2. **API Endpoint:**
   - **POST /transcribe**
     - Accepts an audio file in the request body.
     - Returns a JSON response with the transcription of the audio.

## Example Request

To transcribe an audio file, you can use a tool like `curl` or Postman:

```
curl -X POST -F "file=@path_to_your_audio_file.ogg" http://localhost:5000/transcribe
```

## Response

The API will return a JSON object containing the transcription:

```json
{
    "transcription": "Your transcribed text here."
}
```

## Dependencies

- Flask
- SpeechRecognition

## License

This project is licensed under the MIT License.