import speech_recognition as sr
import speech2emotion

def transcribe_audio(audio_data):
    """Converts speech to text from an in-memory WAV file."""
    recognizer = sr.Recognizer()
    
    with sr.AudioFile(audio_data) as source:
        print("Processing audio for transcription...")
        audio_content = recognizer.record(source)  # Process only the current audio

    try:
        text = recognizer.recognize_google(audio_content)
        #print("Transcription:", text)
        return text
    except sr.UnknownValueError:
        return "Could not understand the audio."
    except sr.RequestError as e:
        return f"Could not request results; {e}"
    
def predict_emo(audio_data):
    return speech2emotion.predict_emotion(audio_data)
    