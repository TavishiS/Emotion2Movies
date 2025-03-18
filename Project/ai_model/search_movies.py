import json
import numpy as np
import faiss
import pandas as pd
from sentence_transformers import SentenceTransformer

# Load movie metadata
with open("data/movies.json", "r", encoding="utf-8") as f:
    movies = json.load(f)

# Load FAISS index
index = faiss.read_index("embeddings/movie_embeddings.faiss")
print(f"FAISS index dimension: {index.d}")
# Load movie ID mapping
with open("embeddings/movie_ids.json", "r", encoding="utf-8") as f:
    movie_ids = json.load(f)

# Load SentenceTransformer model (same one used for embeddings)
MODEL_NAME = "BAAI/bge-large-en"
model = SentenceTransformer(MODEL_NAME)

def search_movies(query, top_k=10):
    """Search for the top-k most relevant movies based on a text query."""
    query = query.replace(" ", "")  # Remove spaces from user input
    prompt = f"{query}"

    query_embedding = model.encode([prompt], convert_to_numpy=True)
    
    # Perform search in FAISS
    print(f"Query embedding dimension: {query_embedding.shape}")

    _, top_indices = index.search(query_embedding, top_k)
    
    # Retrieve the top matching movies
    results = []
    for idx in top_indices[0]:
        movie_id = movie_ids[idx]
        movie_data = next((m for m in movies if m["id"] == movie_id), None)
        if movie_data:
            results.append(movie_data)
    # Remove duplicate movie results by ID
    unique_movies = {}
    for movie in results:
        if movie["id"] not in unique_movies:
            unique_movies[movie["id"]] = movie  # Store unique movies by ID

    # Convert back to a list for display
    filtered_movies = list(unique_movies.values())

    return filtered_movies[:5]

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
        

