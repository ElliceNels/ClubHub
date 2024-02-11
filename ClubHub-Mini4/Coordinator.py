import sqlite3
from Verification import Verification

conn = sqlite3.connect('ClubHub-Mini4\database\Clubhub.db')
cur = conn.cursor()

club_data = cur.execute('''SELECT Club_name,Coordinator_id, Description FROM CLUBS ''')

user_data = cur.execute(''' SELECT Firstname, Lastname, Contact_number FROM USER_DETAILS ''')

for row in user_data:
    print(row)

for row in club_data:
    for column in row:
        coordinator_name = cur.execute(''' SELECT Firstname, Lastname, Contact_number FROM USER_DETAILS WHERE User_id = ? ''', (column[1],))
        print(coordinator_name)


cur.close()
conn.close()