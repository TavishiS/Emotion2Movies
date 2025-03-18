import json
import numpy as np
import requests
import os
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch
import torch.nn.functional as F
from tqdm import tqdm

tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions")

# 🔹 Load movie data
def load_movie_data(file_path="data/movies.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        movies = json.load(f)
    return movies

def load_genre_mapping(file_path="data/genre_mapping.json"):
    with open(file_path, "r", encoding="utf-8") as f:
        genre_mapping = json.load(f)
    return genre_mapping

movies = load_movie_data()
genre_mapping = load_genre_mapping()

# Emotion labels (excluding 'neutral')
emotion_labels = ["admiration", "amusement", "anger", "annoyance", "approval",
                  "caring", "confusion", "curiosity", "desire", "disappointment",
                  "disapproval", "disgust", "embarrassment", "excitement", "fear",
                  "gratitude", "grief", "joy", "love", "nervousness",
                  "optimism", "pride", "realization", "relief", "remorse",
                  "sadness", "surprise"]

def predict_emotions(text, device="cuda" if torch.cuda.is_available() else "cpu"):
    model.to(device)  # Move model to GPU
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True).to(device)
    with torch.no_grad():
        logits = model(**inputs).logits  # Forward pass
        logits = logits[:, :-1]  # Remove last column (neutral)
    probs = F.softmax(logits, dim=-1).squeeze().cpu().tolist()  # Move back to CPU for JSON
    
    # Convert to dict
    emotion_probs = {emotion_labels[i]: probs[i] for i in range(len(emotion_labels))}
    
    return emotion_probs, probs

emotion_encodings = []
print("🔄 Computing emotion encodings...")

# Add tqdm progress bar around the movies loop
for m in tqdm(movies, desc="Processing Movies", unit="movie"):
    genre_names = [genre_mapping.get(str(gid), "") for gid in m.get("genres", [])]
    genre_text = ", ".join(genre_names) if genre_names else ""
    description = m.get("overview", "")
    movie_text = f"{m['title']} ({m['release_date']}) Genre: {genre_text}. Overview: {description}"
    emotion_probs, probs = predict_emotions(movie_text)
    emotion_encodings.append(probs)

os.makedirs("data", exist_ok=True)
with open("data/emotion_encodings.json", "w", encoding="utf-8") as f:
    json.dump(emotion_encodings, f, indent=4, ensure_ascii=False)

print(f"✅ Successfully saved emotion encodings to data/emotion_encodings.json")