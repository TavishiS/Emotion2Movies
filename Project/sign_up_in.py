from flask import request, jsonify
import bcrypt
import flask_login
import userDatabase

class User(flask_login.UserMixin):
    def __init__(self,username):
        self.id=username

def signup():
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validation: Ensure fields are not empty
        if not username or not email or not password:
            return jsonify({"message": "All fields are required!"})
        
        existing_user = userDatabase.collection.find_one({"$or": [{"username": username}, {"email": email}]})

        if existing_user:
            return jsonify({"message": "Username or email already registered!"})  # You can also render an error message in HTML
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {
            "username": username,
            "email": email,
            "password": hashed_password.decode('utf-8'),
            "wishlist": []
        }
        userDatabase.collection.insert_one(user_data)

        return jsonify({"message": "User registered successfully!"})

    except Exception as e:
        return jsonify({"message": "Database error!", "error": str(e)})

def signin():
    try:
        username = request.form.get("username")
        password = request.form.get("password")

        # Validation: Ensure fields are not empty
        if not username or not password:
            return jsonify({"message": "All fields are required!"})

        user = userDatabase.collection.find_one({"username": username})
        if not user:
            return jsonify({"message": "User not found!"})

        if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            return jsonify({"message": "Invalid password!"})

        return jsonify({"message": "User logged in successfully!"})

    except Exception as e:
        return 'Bad login'

