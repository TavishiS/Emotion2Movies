import requests
import json
import os

TMDB_API_KEY = "08f754591935e3223e64fe37680f7ba0"
GENRE_URL = f"https://api.themoviedb.org/3/genre/movie/list?api_key={TMDB_API_KEY}&language=en-US"

# Fetch genres from TMDB
response = requests.get(GENRE_URL)
if response.status_code == 200:
    genre_data = response.json()["genres"]
    genre_mapping = {str(genre["id"]): genre["name"] for genre in genre_data}

    # Save to JSON
    os.makedirs("data", exist_ok=True)
    with open("data/genre_mapping.json", "w", encoding="utf-8") as f:
        json.dump(genre_mapping, f, indent=4, ensure_ascii=False)

    print(f"✅ Successfully saved {len(genre_mapping)} genres to data/genre_mapping.json")

else:
    print(f"⚠️ Failed to fetch genres! Status Code: {response.status_code}")
