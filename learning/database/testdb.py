from pymongo import MongoClient

MONGO_URI = "mongodb+srv://TavishiS:Abcd%2A1234@users.wlgnv.mongodb.net/?retryWrites=true&w=majority&appName=Users"
client = MongoClient(MONGO_URI)

db = client["Users"]
credentials_collection = db["credentials"]

# Insert test data
test_data = {"username": "testuser", "password": "testpass"}
result = credentials_collection.insert_one(test_data)

print("Inserted ID:", result.inserted_id)
