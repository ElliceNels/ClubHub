import sqlite3
from constants import DB_PATH


with sqlite3.connect(DB_PATH) as conn:
    cur = conn.cursor()

    cur.execute(''' CREATE VIEW IF NOT EXISTS USER_INFORMATION AS
        SELECT ud.user_id, ud.firstname, ud.lastname, ul.username, ud.email,contact_number
        FROM USER_DETAILS as ud
        INNER JOIN USER_LOGIN as ul
        ON ud.User_id = ul.User_id; ''')
    
    conn.commit()
    print("User information view created")

    cur.execute('''
        CREATE VIEW IF NOT EXISTS CLUB_AND_MEMBERS AS
        SELECT
            c.Club_name,
            u.User_id,
            u.Firstname,
            u.Lastname
        FROM CLUB_MEMBERSHIP cm
        INNER JOIN CLUBS c ON cm.Club_id = c.Club_id
        INNER JOIN USER_DETAILS u ON cm.User_id = u.User_id;
    ''')
    
    conn.commit()
    print("Club membership view created successfully")