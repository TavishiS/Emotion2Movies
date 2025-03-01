from pymongo import MongoClient

# Replace with your MongoDB URI
client = MongoClient("mongodb+srv://TavishiS:Abcd*1234@users.wlgnv.mongodb.net/")
db = client["Users"]
users_collection = db["users"]

def save_user(username, email, password):
    users_collection.insert_one({"username": username, "email": email, "password": password})
    return "User saved!"

# Example usage
save_user("john_doe", "john@example.com", "securepassword123")
