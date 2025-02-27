from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
from using_deepseek_remote import prompt2movie
import requests

app=Flask(__name__)
CORS(app)  # This line enables Cross-Origin Resource Sharing (CORS) for the Flask app, allowing resources to be requested from another domain.

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

@app.route('/')
def firstPage():
    return render_template('about.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/form_input')
def form_input():
    return render_template('form_input.html')

@app.route('/recommend_form', methods=['GET'])
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

@app.route('/prompt_input')
def prompt_input():
    return render_template('prompt_input.html')

@app.route('/prompt_generate', methods=['GET','POST'])
def prompt_generate():
    prompt_in = request.form['prompt']
    print(prompt_in)
    movie_names = prompt2movie.give3movies(prompt=prompt_in)
    print(movie_names)
    trailer_urls = []
    for movie_name in movie_names:
        trailer_url = f"https://www.youtube.com/results?search_query=trailer+%3A+{movie_name}"
        trailer_urls.append(trailer_url)
    return render_template('recommendations.html', movies_urls=zip(movie_names, trailer_urls))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)