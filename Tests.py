import sqlite3

conn = sqlite3.connect(DB_PATH)
cursor = conn.cursor()
#Execute a query to retrieve data
cursor.execute('''SELECT Password, User_id FROM USER_LOGIN WHERE Login_id BETWEEN ? AND ?''', (1, 4))


username = cursor.fetchall()
# Fetch all rows of data
for row in username:
    for column in row:
        print(column)



#print(cursor)
#print(username)

# Close the database connection
conn.close()