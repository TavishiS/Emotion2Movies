from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
import bcrypt

uri = "mongodb+srv://TavishiS:Abcd%2A1234@users.wlgnv.mongodb.net/?retryWrites=true&w=majority&appName=Users"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Users"]
collection = db["credentials"]

collection.update_many(
    {"wishlist": {"$exists": False}},  # Only update documents that don't have 'wishlist'
    {"$set": {"wishlist": []}}  # Initialize as an empty array
)

def display_data():
    i=0
    for user in collection.find():
        i+=1
        print("-------------------------------------------------------")
        print(str(i)+".","user _id: ",user['_id'])
        print("\tuser username: ",user['username'])
        print("\tuser email   : ",user['email'])
        print("\tuser password: ",user['password'])
        print('\tuser wishlist: ',user['wishlist'])
    print("-------------------------------------------------------")
    print("\nTotal users: ",i,"\n")
    print("-------------------------------------------------------")
    # Close the connection

def add_to_wishlist(user_name, movie):
    # for movie in movies_list:
        if not is_movie_in_wishlist(user_name, movie):
            collection.update_one(
                {"username": user_name},
                {"$push": {"wishlist": movie}}        
        )
            

def is_movie_in_wishlist(user_name, movie_name):
    """Check if a movie is already in the user's wishlist."""
    user = collection.find_one({"username": user_name, "wishlist": movie_name})
    return user is not None  # Returns True if movie exists, False otherwise

def remove_from_wishlist(user_name, movie_name):
    if is_movie_in_wishlist(user_name, movie_name):
        collection.update_one(
            {"username": user_name},
            {"$pull": {"wishlist":movie_name}}
        )

def clear_wishlist(user_name):
    if collection.find_one({"username": user_name}):
        collection.update_one({"username": user_name},{"$set": {"wishlist": []}})

def update_password(user_name, old_password, new_password, recheck_new_password):
    user = collection.find_one({"username": user_name})
    if user:
        if not bcrypt.checkpw(old_password.encode('utf-8'), user["password"].encode('utf-8')): # comparing old password binary with database password binary
            return "Old password mismatch"
        elif new_password != recheck_new_password:               
            return "New password and Confirm password mismatch"
        else:          
            hashed_ = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt())
            collection.update_one(
            {"username" : user_name}, {"$set" :{"password" : hashed_.decode('utf-8')}}
            )
            return "Password changed successfully"
        
def delete_user(user_name):
    collection.delete_one({"username": user_name})
    
if __name__ == "__main__":
    # add_to_wishlist("tavi", "aunty no 1")
    # clear_wishlist("tavi")
    # remove_from_wishlist("tavi", "Allah hu akbar")
    # remove_from_wishlist("tavi", "bajirao mastani")
    # print(update_password("tavi", "kashish", "girl", "girl"))
    # delete_user("tavivi")
    
    #collection.delete_one({"username": "shree123"}) #delete a user if found
    #collection.delete_many({}) # to delte all users
    display_data()
    
    