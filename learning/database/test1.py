from pymongo import MongoClient
client = MongoClient("mongodb+srv://TavishiS:Abcd%2A1234@users.wlgnv.mongodb.net/?retryWrites=true&w=majority&appName=Users")
print(client.list_database_names())  # Should print your database names
