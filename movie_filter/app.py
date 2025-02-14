from flask import Flask, request, jsonify
from flask_cors import CORS
import requests

app = Flask(__name__)
CORS(app)

TMDB_API_KEY = "08f754591935e3223e64fe37680f7ba0"

def get_movie_trailer(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}/videos?api_key={TMDB_API_KEY}"
    try:
        response = requests.get(url).json()
        if "results" in response:
            for video in response["results"]:
                if video["site"] == "YouTube" and video["type"] == "Trailer":
                    return video['key']
        return None
    except Exception as e:
        print(f"Error fetching trailer: {e}")
        return None

@app.route('/recommend', methods=['GET'])
def recommend_movies():
    # Get parameters from query string
    genre = request.args.get("genre", "")
    language = request.args.get("language", "")
    rating_min = request.args.get("minRating", 0)
    rating_max = request.args.get("maxRating", 10)
    year_min = request.args.get("startYear", 1900)
    year_max = request.args.get("endYear", 2025)
    duration_min = request.args.get("minDuration", 0)
    duration_max = request.args.get("maxDuration", 300)

    url = f"https://api.themoviedb.org/3/discover/movie"
    params = {
        "api_key": TMDB_API_KEY,
        "with_genres": genre,
        "with_original_language": language,
        "vote_average.gte": rating_min,
        "vote_average.lte": rating_max,
        "primary_release_date.gte": f"{year_min}-01-01",
        "primary_release_date.lte": f"{year_max}-12-31",
        "with_runtime.gte": duration_min,
        "with_runtime.lte": duration_max,
        "sort_by": "popularity.desc"
    }

    try:
        response = requests.get(url, params=params).json()
        movies = response.get("results", [])[:5]

        recommended_movies = []
        for movie in movies:
            trailer_key = get_movie_trailer(movie["id"])
            recommended_movies.append({
                "title": movie["title"],
                "year": movie["release_date"][:4] if movie.get("release_date") else "N/A",
                "rating": round(movie["vote_average"], 1) if movie.get("vote_average") else "N/A",
                "trailer": trailer_key
            })

        return jsonify({"movies": recommended_movies})
    except Exception as e:
        print(f"Error in recommend_movies: {e}")
        return jsonify({"error": "Failed to fetch movies"}), 500

if __name__ == '__main__':
    app.run(debug=True)