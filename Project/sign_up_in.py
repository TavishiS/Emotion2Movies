from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi
import bcrypt

app = Flask(__name__)

# Correct MongoDB Connection String (Update your password!)
MONGO_URI = "mongodb+srv://TavishiS:Abcd%2A1234@users.wlgnv.mongodb.net/?retryWrites=true&w=majority&appName=Users"
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())  
db = client["Users"]  # Database
credentials_collection = db["credentials"]  # Collection

def signup():
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validation: Ensure fields are not empty
        if not username or not email or not password:
            return jsonify({"message": "All fields are required!"})
        
        existing_user = credentials_collection.find_one({"$or": [{"username": username}, {"email": email}]})

        if existing_user:
            return jsonify({"message": "Username or email already registered!"})  # You can also render an error message in HTML
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
        user_data = {"username": username, "email": email, "password": hashed_password.decode('utf-8')}
        credentials_collection.insert_one(user_data)

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

        user = credentials_collection.find_one({"username": username})

        if not user:
            return jsonify({"message": "User not found!"})

        if not bcrypt.checkpw(password.encode('utf-8'), user["password"].encode('utf-8')):
            return jsonify({"message": "Invalid password!"})

        return jsonify({"message": "User logged in successfully!"})

    except Exception as e:
        return jsonify({"message": "Database error!", "error": str(e)})

# Test MongoDB Connection (To check if MongoDB is working)
# @app.route('/test-db')
# def test_db():
#     try:
#         credentials_collection.insert_one({"username": "test", "email": "test@test.com", "password": "test"})
#         return "MongoDB Connection Successful! Test user added."
#     except Exception as e:
#         return f"MongoDB Error: {str(e)}"

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
