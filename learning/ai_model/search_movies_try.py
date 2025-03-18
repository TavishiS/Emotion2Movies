import json
import numpy as np
import faiss
import torch
from sentence_transformers import SentenceTransformer
from sklearn.metrics.pairwise import cosine_similarity
from transformers import AutoTokenizer, AutoModelForSequenceClassification
import torch.nn.functional as F

# Constants
WEIGHT_FAISS = 0.3
WEIGHT_GENRE = 0.35
WEIGHT_EMOTION = 0.35
MODEL_NAME = "BAAI/bge-large-en"
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# Load all data at startup
def load_data():
    # Load movie metadata
    with open("data/movies.json", "r", encoding="utf-8") as f:
        movies = json.load(f)
    
    # Create movie_id to movie mapping for efficient lookup
    movie_dict = {movie["id"]: movie for movie in movies}
    
    # Load FAISS index
    index = faiss.read_index("embeddings/movie_embeddings.faiss")
    
    # Load movie ID mapping
    with open("embeddings/movie_ids.json", "r", encoding="utf-8") as f:
        movie_ids = json.load(f)
    
    # Load emotion encodings
    with open("data/emotion_encodings.json", "r", encoding="utf-8") as f:
        emotion_encodings = json.load(f)
    
    # Load genre encodings
    with open("data/genre_encodings.json", "r", encoding="utf-8") as f:
        genre_encodings = json.load(f)
    
    # Load genre mapping
    with open("data/genre_mapping.json", "r", encoding="utf-8") as f:
        genre_mapping = json.load(f)
    
    genre_names = {v.lower(): k for k, v in genre_mapping.items()}
    
    return movies, movie_dict, index, movie_ids, emotion_encodings, genre_encodings, genre_mapping, genre_names

# Load models at startup
def load_models():
    # Load SentenceTransformer model
    sentence_model = SentenceTransformer(MODEL_NAME)
    
    # Load emotion model
    emotion_tokenizer = AutoTokenizer.from_pretrained("SamLowe/roberta-base-go_emotions")
    emotion_model = AutoModelForSequenceClassification.from_pretrained("SamLowe/roberta-base-go_emotions").to(DEVICE)
    
    return sentence_model, emotion_tokenizer, emotion_model

# Emotion labels (excluding 'neutral')
emotion_labels = ["admiration", "amusement", "anger", "annoyance", "approval",
                  "caring", "confusion", "curiosity", "desire", "disappointment",
                  "disapproval", "disgust", "embarrassment", "excitement", "fear",
                  "gratitude", "grief", "joy", "love", "nervousness",
                  "optimism", "pride", "realization", "relief", "remorse",
                  "sadness", "surprise"]

# Load all data and models once
movies, movie_dict, index, movie_ids, emotion_encodings, genre_encodings, genre_mapping, GENRE_NAMES = load_data()
sentence_model, emotion_tokenizer, emotion_model = load_models()

def search_movies(query, top_k=10):
    # Compute query text embedding
    query_embedding = sentence_model.encode([query], convert_to_numpy=True)
    
    # Perform FAISS search
    faiss_distances, top_indices = index.search(query_embedding, top_k)
    
    # Compute query emotion encoding
    inputs = emotion_tokenizer(query, return_tensors="pt", truncation=True, padding=True).to(DEVICE)
    with torch.no_grad():
        logits = emotion_model(**inputs).logits  # Forward pass
        logits = logits[:, :-1]  # Remove last column (neutral)
    probs = F.softmax(logits, dim=-1).squeeze().cpu().numpy()  # Convert to numpy array
    
    query_emotion = probs

    # Compute query genre encoding
    query_lower = query.lower()
    genre_vector = np.zeros(len(genre_mapping))
    
    for idx, genre in enumerate(GENRE_NAMES.keys()):
        if genre in query_lower:
            genre_vector[idx] = 1 

    query_genre = genre_vector
    
    unique_movies = {}
    
    # Normalize FAISS distances to [0,1] - keep the array structure
    max_faiss = np.max(faiss_distances) if faiss_distances.size > 0 else 1
    normalized_faiss_distances = faiss_distances[0] / max_faiss if max_faiss > 0 else faiss_distances[0]

    for rank, idx in enumerate(top_indices[0]):
        movie_id = movie_ids[idx]
        if movie_id in unique_movies:
            continue
            
        movie_data = movie_dict.get(movie_id)
        
        if movie_data:
            # Compute Emotion Euclidean Distance
            movie_emotion = np.array(emotion_encodings[idx])
            emotion_distance = np.linalg.norm(query_emotion - movie_emotion)
            # Normalize emotion distance to [0,1] range
            emotion_distance = min(emotion_distance, 1.0)  # Cap at 1.0

            # Compute Genre Cosine Similarity
            movie_genre = np.array(genre_encodings[idx])
            genre_similarity = cosine_similarity([query_genre], [movie_genre])[0][0]  # Cosine similarity
            
            # Compute final score - lower is better for all components
            final_score = (
                (WEIGHT_FAISS * normalized_faiss_distances[rank]) + 
                (WEIGHT_GENRE * (1 - genre_similarity)) + 
                (WEIGHT_EMOTION * emotion_distance)
            )

            unique_movies[movie_id] = (final_score, movie_data)
    
    # Sort by final score (ascending, lower is better)
    sorted_results = sorted(unique_movies.values(), key=lambda x: x[0])

    # Get top 5 movies
    filtered_movies = [movie for _, movie in sorted_results[:5]]
    return filtered_movies

if __name__ == "__main__":
    while True:
        user_input = input("Enter a movie-related query (or type 'exit' to quit): ")
        if user_input.lower() == "exit":
            break

        results = search_movies(user_input)
        if results:
            print("\nTop Matching Movies:")
            for i, movie in enumerate(results, start=1):
                print(f"{i}. {movie['title']} ({movie.get('release_date', 'N/A')})")
                print(f"   Overview: {movie.get('description', 'No description available.')}\n")
        else:
            print("No matching movies found. Try a different query.")