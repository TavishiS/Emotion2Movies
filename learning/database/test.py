import sqlite3

conn = sqlite3.connect("instance/users.db")  # Adjust path if needed
cursor = conn.cursor()

# Get the list of all tables in the database
cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
tables = cursor.fetchall()

print("Tables in database:", tables)

conn.close()
