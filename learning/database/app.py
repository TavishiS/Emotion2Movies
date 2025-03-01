from flask import Flask, render_template, request, jsonify
from pymongo import MongoClient
import certifi

app = Flask(__name__)

# ✅ Correct MongoDB Connection String (Update your password!)
MONGO_URI = "mongodb+srv://TavishiS:Abcd%2A1234@users.wlgnv.mongodb.net/?retryWrites=true&w=majority&appName=Users"
client = MongoClient(MONGO_URI, tlsCAFile=certifi.where())  
db = client["Users"]  # Database
credentials_collection = db["credentials"]  # Collection

# ✅ Home Route (Renders Signup Page)
@app.route('/')
def home():
    return render_template('index.html')

# ✅ Signup Route (Handles Form Submission)
@app.route('/signup', methods=['POST'])
def signup():
    try:
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        # Validation: Ensure fields are not empty
        if not username or not email or not password:
            return jsonify({"message": "All fields are required!"}), 400
        
        existing_user = credentials_collection.find_one({"$or": [{"username": username}, {"email": email}]})

        if existing_user:
            return jsonify({"message": "Username or email already registered!"})  # You can also render an error message in HTML

        # ✅ Insert into MongoDB
        user_data = {"username": username, "email": email, "password": password}
        credentials_collection.insert_one(user_data)

        return jsonify({"message": "User registered successfully!"})

    except Exception as e:
        return jsonify({"message": "Database error!", "error": str(e)}), 500

# ✅ Test MongoDB Connection (To check if MongoDB is working)
@app.route('/test-db')
def test_db():
    try:
        credentials_collection.insert_one({"username": "test", "email": "test@test.com", "password": "test"})
        return "MongoDB Connection Successful! Test user added."
    except Exception as e:
        return f"MongoDB Error: {str(e)}"

if __name__ == '__main__':
    # app.run(debug=True)
    app.run(host="0.0.0.0", port=5000, debug=True)
