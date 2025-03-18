import json
import numpy as np
import requests
import json
import os

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
genre_encodings = []

genre_index = {genre_id: i for i, (genre_id, genre_name) in enumerate(genre_mapping.items())}

for m in movies:
    genre_encoding = np.zeros(19)
    genres = m.get("genres",[])
    for genre in genres:
        genre_str = str(genre)
        genre_encoding[genre_index[genre_str]]=1
    genre_encodings.append(genre_encoding.tolist())

os.makedirs("data", exist_ok=True)
with open("data/genre_encodings.json", "w", encoding="utf-8") as f:
    json.dump(genre_encodings, f, indent=4, ensure_ascii=False)

print(f"✅ Successfully saved genre encodings to data/genre_encodings.json")