from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
import sign_up_in
import flask_login
import pymongo
import prompt2movie, form2movie, userDatabase

app=Flask(__name__) #initializing flask app

CORS(app)#enables cross origin resource sharing
app.secret_key = 'SE_project'  # Change this to your secret key
login_manager = flask_login.LoginManager()
login_manager.init_app(app)

#user class
class User(flask_login.UserMixin):
    def __init__(self,username):
        self.id=username
        self.email = userDatabase.collection.find_one({"username": username})['email']
        self.password = userDatabase.collection.find_one({"username": username})['password']
        self.wishlist = userDatabase.collection.find_one({"username": username})['wishlist']

@login_manager.user_loader
def user_loader(username):  #this will be more related to our project
    #users = userDatabase.collection.find_one({"username": username})
    if not userDatabase.collection.find_one({"username": username}):
        return None
    user = User(username)
    return user

@login_manager.request_loader # mainly used for API authentication
def request_loader(request): 
    #users = userDatabase.collection.find_one({"username": username})
    username = request.form.get('username')
    if not userDatabase.collection.find_one({"username": username}):
        return None
    user = User(username)
    return user

#first page of app
@app.route('/')
def firstPage():
    return render_template('about.html')

#guest page
@app.route('/home_guest')
def home():
    return render_template('home_guest.html')

#sign up page
@app.route('/sign_up')
def sign_up():
    return render_template('sign_up.html')

#triggered on clicking signup button , allowed methods are only get and post
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

#sign in page
@app.route('/sign_in')
def sign_in():
    return render_template('sign_in.html')

#triggered when clicked sign in button , allowed methods are only get and post
@app.route('/signin', methods=['GET', 'POST'])
def login():
    signin_message = sign_up_in.signin()
    signin_message_data = signin_message.get_json()
    if signin_message_data.get('message')=='bad login':
        return 'Bad login'
    if signin_message_data.get('message')=='User logged in successfully!':
        username = request.form.get('username')
        user = User(username)
        flask_login.login_user(user)
        return redirect(url_for('protected'))
    else:
        flash(signin_message_data.get('message'), 'error')
        return redirect(url_for('sign_in'))
    
#home of user which is logged in
@app.route('/home_user')
@flask_login.login_required
def protected():
    #renders webpage with current user data
    return render_template('home_user.html', user=flask_login.current_user)
#form input of user
@app.route('/form_input')
@flask_login.login_required
def form_input():
    return render_template('form_input.html')

#triggers on submitting the form
@app.route('/recommend_form', methods=['GET'])
@flask_login.login_required
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
@flask_login.login_required
def prompt_input():
    return render_template('prompt_input.html',user=flask_login.current_user)

@app.route('/prompt_generate', methods=['GET','POST'])
@flask_login.login_required
def prompt_generate():
    prompt_in = request.form['prompt']
    print(prompt_in)
    movie_names = prompt2movie.give5movies(prompt=prompt_in)
    print(movie_names)
    trailer_urls = []
    for movie_name in movie_names:
        trailer_url = f"https://www.youtube.com/results?search_query=trailer+%3A+{movie_name}"
        trailer_urls.append(trailer_url)
    return render_template('recommendations.html', movies_urls=zip(movie_names, trailer_urls))

#logout action after clicking logout button , renders about.html page and logs user out
@app.route('/logout')
def logout():
    flask_login.logout_user()
    return render_template('about.html')

@login_manager.unauthorized_handler
def unauthorized_handler():
    return 'Unauthorized access', 401

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000)