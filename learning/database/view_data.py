import sqlite3

conn = sqlite3.connect("E:/database/instance/users.db")  # Adjust path if needed
cursor = conn.cursor()

cursor.execute("SELECT * FROM user")  # Change 'users' to your actual table name
data = cursor.fetchall()

for row in data:
    print(row)

conn.close()
