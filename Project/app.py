from flask import Flask, render_template, request, jsonify, redirect, url_for, flash
from flask_cors import CORS
import sign_up_in
import flask_login
import prompt2movie, form2movie, userDatabase #importing .py files (modules)
from pydub import AudioSegment
import process_audio
import io
from ai_model import search_movies_try

########################################################################################################

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

########################################################################################################

#first page of app
@app.route('/')
def firstPage():
    return render_template('about4guest.html')

#guest page
@app.route('/home_guest')
def home():
    return render_template('home_guest.html')

@app.route("/contact_us_guest")
def contact_us_guest():
    return render_template("contact_us_guest.html")

########################################################################################################

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

########################################################################################################
@app.route('/about4user')
@flask_login.login_required
def about4user():
    return render_template('about4user.html', user=flask_login.current_user)
#home of user which is logged in
@app.route('/home_user')
@flask_login.login_required
def protected():
    #renders webpage with current user data
    return render_template('home_user.html', user=flask_login.current_user)
@app.route('/profile')
@flask_login.login_required
def show_user_profile():
    return render_template("profile.html", user=flask_login.current_user)

# Route to render the change password page
@app.route('/change_password', methods=['GET'])
def change_password_page():
    return render_template('change_password.html', user=flask_login.current_user)

# Route to handle the password change request
@app.route('/change_password', methods=['POST'])
def change_password():
    data = request.json
    username = data.get("username")
    old_password = data.get("old_password")
    new_password = data.get("new_password")
    recheck_new_password = data.get("recheck_new_password")

    if new_password != recheck_new_password:
        return jsonify({"message": "New passwords do not match!"})

    # Call function to update password
    result = userDatabase.update_password(username, old_password, new_password, recheck_new_password)
    return jsonify({"message": result})

@app.route("/contact_us_user")
def contact_us_user():
    return render_template("contact_us_user.html")

##########################################################################################################

#form input of user
@app.route('/form_input')
@flask_login.login_required
def form_input():
    return render_template('form_input.html')

#triggers on submitting the form
@app.route('/recommend_form', methods=['GET','POST'])
@flask_login.login_required
def recommend_movies():
    # Get parameters from query string
    genre = request.form.get("genre", "")
    language = request.form.get("language", "")
    rating_min = int(request.form.get("minRating", 0))
    rating_max = int(request.form.get("maxRating", 10))
    year_min = int(request.form.get("startYear", 1900))
    year_max = int(request.form.get("endYear", 2025))
    duration_min = int(request.form.get("minDuration", 0))
    duration_max = int(request.form.get("maxDuration", 300))
    movies= form2movie.recommand_movies(genre, language, rating_min, rating_max, year_min, year_max, duration_min, duration_max)
    movies= movies.get_json().get('movies', [])
    made_prompt = f"Movies with genre {genre}, language {language}, rating between {rating_min} and {rating_max}, year between {year_min} and {year_max}, duration between {duration_min} and {duration_max}"
    trailer_keys = []
    for movie in movies:
        trailer_keys.append(movie['trailer'])
    movie_list = userDatabase.collection.find_one({"username": flask_login.current_user.id})['wishlist']
    
    return render_template('recommendations.html', movie_data=movies, trailer_keys=trailer_keys, given_prompt=made_prompt,wishlist_movies=movie_list , user=flask_login.current_user)

##########################################################################################################    
@app.route('/prompt_input')
@flask_login.login_required
def prompt_input():
    return render_template('prompt_input.html',user=flask_login.current_user)

##########################################################################################################

@app.route('/prompt_input_speech')
@flask_login.login_required
def prompt_input_speech():
    return render_template('prompt_input_speech.html',user=flask_login.current_user)

@app.route('/process_audio_input', methods=['POST'])
@flask_login.login_required
def upload():
    """Handles audio file uploads without saving."""
    audio_file = request.files['audio']
    
    if not audio_file:
        return jsonify({"error": "No audio file provided"}), 400

    try:
        # Convert from webm to wav in memory
        audio = AudioSegment.from_file(audio_file.stream, format="webm")
        audio = audio.set_channels(1).set_frame_rate(16000)

        # Save to in-memory bytes buffer
        wav_io = io.BytesIO()
        audio.export(wav_io, format="wav")
        wav_io.seek(0)

        # Transcribe the audio
        text = process_audio.transcribe_audio(wav_io)

        # Reset buffer for emotion prediction
        wav_io.seek(0)
        pred_emo = process_audio.predict_emo(wav_io)
        print(f"Predicted Emotion: {pred_emo}")
        return jsonify({"message": "Processing complete", "transcription": text, "emotion": pred_emo})
    
    except Exception as e:
        return jsonify({"error": f"Processing failed: {e}"}), 500

##########################################################################################################  
  
@app.route('/prompt_send_to_model', methods=['GET','POST'])
@flask_login.login_required
def prompt_send_to_model():
    try :
        prompt_in = request.form.get('prompt', '')
        return redirect(url_for('model_run', prompt=prompt_in))
    
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('prompt_input'))
    
@app.route('/prompt_process_with_API_and_send_to_model', methods=['GET','POST'])
@flask_login.login_required
def prompt_process_with_API_and_send_to_model():
    try :
        prompt_in = request.form.get('prompt', '')
        prompt_in += " related movies, not exactly same"
        print(prompt_in)

        movie_names = prompt2movie.give5movies(prompt=prompt_in)
        prompt_processed = ""
        for movie_name in movie_names:
            prompt_processed += movie_name + ", "
        return redirect(url_for('model_run', prompt=prompt_processed))
    except Exception as e:
        print(f"Error: {e}")
        return redirect(url_for('prompt_input'))

##########################################################################################################

@app.route('/model_run', methods=['GET', 'POST'])
@flask_login.login_required
def model_run():
    try:
        prompt_in = request.args.get('prompt', '')  
        #taking input from /prompt_send_to_model or from /prompt_process_with_API_and_send_to_model
        print(prompt_in)
        movie_data, movie_ids = search_movies_try.search_movies(prompt_in)
        trailer_keys = form2movie.promptID_to_movie(movie_ids)  # Get trailer keys as a list
        movie_list = userDatabase.collection.find_one({"username": flask_login.current_user.id})['wishlist']
        
    except Exception as e:
        print(f"Error: {e}")
        trailer_keys = []
        movie_data = []
        movie_list = []
    return render_template('recommendations.html', movie_data=movie_data, trailer_keys=trailer_keys, given_prompt=prompt_in,wishlist_movies=movie_list , user=flask_login.current_user)

##########################################################################################################
@app.route("/add_to_wishlist", methods=["POST"])
@flask_login.login_required
def add_to_wishlist():
    try:
        data = request.get_json()
        movie_title = data.get("movie_title")

        if not movie_title:
            return jsonify({"error": "Movie title is required"}), 400

        userDatabase.add_to_wishlist(flask_login.current_user.id, movie_title)
        movie_list = userDatabase.collection.find_one({"username": flask_login.current_user.id})['wishlist']
        return jsonify({"message": f"'{movie_title}' added to wishlist", "wishlist": movie_list}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route("/remove_from_wishlist", methods=["POST"])
@flask_login.login_required
def remove_from_wishlist():
    try:
        data = request.get_json()
        movie_title = data.get("movie_title")

        if not movie_title:
            return jsonify({"error": "Movie title is required"}), 400

        movie_list = userDatabase.collection.find_one({"username": flask_login.current_user.id})['wishlist']
        if movie_title in movie_list:
            userDatabase.remove_from_wishlist(flask_login.current_user.id, movie_title)
            movie_list = userDatabase.collection.find_one({"username": flask_login.current_user.id})['wishlist']
            return jsonify({"message": f"'{movie_title}' removed from wishlist", "wishlist": movie_list})
        else:
            return jsonify({"error": f"'{movie_title}' not found in wishlist"}), 404

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    
@app.route("/clear_wishlist", methods=["POST"])
@flask_login.login_required
def clear_wishlist():
    try:
        userDatabase.clear_wishlist(flask_login.current_user.id)
        return jsonify({"message": "Wishlist cleared"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

##########################################################################################################

#logout action after clicking logout button , renders about.html page and logs user out
@app.route('/logout')
@flask_login.login_required
def logout():
    flask_login.logout_user()
    return redirect(url_for('firstPage'))
    

@login_manager.unauthorized_handler
def unauthorized_handler():
    return redirect(url_for('firstPage'))

if __name__ == '__main__':
    app.run(debug=True,host='0.0.0.0',port=5000, threaded=True) #running the app on localhost:5000