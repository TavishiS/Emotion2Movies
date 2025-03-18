import requests
import json
import time
from tqdm import tqdm
import os

# 🔹 Replace with your TMDB API Key
TMDB_API_KEY = "08f754591935e3223e64fe37680f7ba0"

# 🔹 Base URL for TMDB API
BASE_URL = "https://api.themoviedb.org/3/movie/popular"

# 🔹 Create data directory if not exists
os.makedirs("data", exist_ok=True)

# Function to fetch movie data
def fetch_movies(pages=500):
    movies = []
    
    for page in tqdm(range(1, pages + 1), desc="Fetching movies from TMDB"):
        url = f"{BASE_URL}?api_key={TMDB_API_KEY}&language=en-US&page={page}"
        response = requests.get(url)

        if response.status_code == 200:
            data = response.json()
            for movie in data.get("results", []):
                movies.append({
                    "id": movie["id"],
                    "title": movie["title"],
                    "genres": movie.get("genre_ids", []),
                    "release_date": movie.get("release_date", "Unknown"),
                    "popularity": movie.get("popularity", 0),
                    "description": movie.get("overview", "No description available")  # 🔹 Fetch description
                })
        else:
            print(f"⚠️ Error fetching page {page}: {response.status_code}")

        time.sleep(0.2)  # 🔹 Prevent hitting TMDB rate limits

    return movies

# Fetch and save movies with enriched descriptions
movie_data = fetch_movies(pages=500)

# Save to JSON file
with open("data/movies.json", "w", encoding="utf-8") as f:
    json.dump(movie_data, f, indent=4, ensure_ascii=False)

print(f"✅ Successfully saved {len(movie_data)} movies to data/movies.json")