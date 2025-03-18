import json
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer
from tqdm import tqdm
import os

# 🔹 Load the embedding model (BGE-Large)
MODEL_NAME = "BAAI/bge-large-en"
model = SentenceTransformer(MODEL_NAME, device="cuda")

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

# 🔹 Extract movie overviews & IDs with improved formatting
movie_texts = []
for m in movies:
    genre_names = [genre_mapping.get(str(gid), "Unknown") for gid in m.get("genres", [])]
    genre_text = ", ".join(genre_names) if genre_names else "Unknown"
    description = m.get("overview", "No description available")
    movie_texts.append(f"{m['title']} ({m['release_date']}) Genre: {genre_text}. Overview: {description}")

movie_ids = [m["id"] for m in movies]

# 🔹 Compute embeddings
print("🔄 Computing movie embeddings...")
embeddings = model.encode(movie_texts, batch_size=32, convert_to_numpy=True, show_progress_bar=True)

# 🔹 Create FAISS index
embedding_dim = embeddings.shape[1]
index = faiss.IndexFlatL2(embedding_dim)
index.add(embeddings)

# 🔹 Save FAISS index & movie IDs
os.makedirs("embeddings", exist_ok=True)
faiss.write_index(index, "embeddings/movie_embeddings.faiss")

with open("embeddings/movie_ids.json", "w", encoding="utf-8") as f:
    json.dump(movie_ids, f)

print(f"✅ Embeddings saved! Indexed {len(movie_texts)} movies.")
