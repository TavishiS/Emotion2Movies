from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
import requests
import prompt2movie, form2movie
import sign_up_in

app=Flask(__name__)
CORS(app)  # This line enables Cross-Origin Resource Sharing (CORS) for the Flask app, allowing resources to be requested from another domain.

app.secret_key = 'your_secret_key'  # Change this to your secret key

user_name = ""

@app.route('/')
def firstPage():
    return render_template('about.html')

@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

@app.route('/signin', methods=['GET','POST'])
def call_signin():
    return_mess=sign_up_in.signin()
    return_mess_data = return_mess.get_json()
    message = return_mess_data.get('message', '')
    if return_mess_data.get('message')=='User logged in successfully!':
        print(message)
        return redirect(url_for('home'))
    else:
        flash(message, 'error')
        return redirect(url_for('sign_in'))
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

@app.route('/signup', methods=['GET','POST'])
def call_signup():
    return_mess=sign_up_in.signup()
    return_mess_data = return_mess.get_json()
    message = return_mess_data.get('message', '')
    if return_mess_data.get('message')=='User registered successfully!':
        flash(message, 'success')
        return redirect(url_for('sign_in'))
    else:
        flash(message, 'error')
        return redirect(url_for('sign_up'))
    
    

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

    return form2movie.recommand_movies(genre, language, rating_min, rating_max, year_min, year_max, duration_min, duration_max)
    

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