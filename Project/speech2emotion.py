import torch
import librosa
from transformers import Wav2Vec2FeatureExtractor, Wav2Vec2ForSequenceClassification, Trainer, TrainingArguments

# Load the pretrained model and feature extractor
MODEL_PATH = "superb/wav2vec2-base-superb-er"  # Using the specified model
feature_extractor = Wav2Vec2FeatureExtractor.from_pretrained(MODEL_PATH)
model = Wav2Vec2ForSequenceClassification.from_pretrained(MODEL_PATH, num_labels=7, ignore_mismatched_sizes=True)
model.eval()

# Define emotion labels (ensure this matches your training labels)
inverse_label_map = {0: 'sad', 1: 'neutral', 2: 'angry', 3: 'happy', 4: 'fear', 5: 'surprise', 6: 'disgust'}

def preprocess_audio(audio_file):
    """Load and preprocess audio."""
    speech, sr = librosa.load(audio_file, sr=16000)  # Ensure 16kHz sample rate
    speech = librosa.util.normalize(speech)  # Normalize audio
    return speech

def predict_emotion(audio_file):
    """Predict emotion from an audio file."""
    speech = preprocess_audio(audio_file)

    # Process audio
    inputs = feature_extractor(speech, sampling_rate=16000, return_tensors="pt", padding=True)
    with torch.no_grad():
        logits = model(**inputs).logits

    # Get predicted label
    predicted_class = torch.argmax(logits, dim=-1).item()
    emotion = inverse_label_map.get(predicted_class, "Unknown")

    return emotion

if __name__ == "__main__":
    # Example usage
    audio_path = "fear.wav"  # Change this to your input file
    predicted_emotion = predict_emotion(audio_path)
    print(f"Predicted Emotion: {predicted_emotion}")