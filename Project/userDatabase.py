from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

uri = "mongodb+srv://TavishiS:Abcd%2A1234@users.wlgnv.mongodb.net/?retryWrites=true&w=majority&appName=Users"

# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi('1'))
db = client["Users"]
collection = db["credentials"]

def display_data():
    i=0
    for user in collection.find():
        i+=1
        print("-------------------------------------------------------")
        print(str(i)+".","user _id: ",user['_id'])
        print("\tuser username: ",user['username'])
        print("\tuser email   : ",user['email'])
        print("\tuser password: ",user['password'])
    print("-------------------------------------------------------")
    print("\nTotal users: ",i,"\n")
    print("-------------------------------------------------------")
    # Close the connection
    
if __name__ == "__main__":
    #collection.delete_one({"username": "shree123"}) #delete a user if found
    #collection.delete_many({}) # to delte all users
    display_data()
    
    