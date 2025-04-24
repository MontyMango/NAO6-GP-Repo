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
