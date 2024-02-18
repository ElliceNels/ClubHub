import sqlite3
conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')
cursor = conn.cursor()
cursor.execute(''' CREATE VIEW IF NOT EXISTS USER_INFORMATION AS
SELECT ud.user_id, ud.firstname, ud.lastname, ul.username, ud.email,contact_number
FROM USER_DETAILS as ud
INNER JOIN USER_LOGIN as ul
ON ud.User_id = ul.User_id; ''')
conn.commit()
print("User information view created")
cursor.close()
conn.close()