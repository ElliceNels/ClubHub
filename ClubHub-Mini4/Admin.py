import sqlite3
from itertools import chain

class Admin:
    def __init__(self):
        self.userList = []
        
    def getUserList(self):
        conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')
        cursor = conn.cursor()
        print("db connected")
        cursor.execute(''' SELECT User_id, Firstname, Lastname FROM USER_DETAILS WHERE Is_pending = ? AND Is_approved = ?''', (1, 0))
        self.userList = [list(row) for row in cursor.fetchall()]
       
        for user in self.userList:
            cursor.execute(''' SELECT User_id FROM COORDINATORS Where User_id = ?''', (int(user[0]),))
            if cursor.fetchone():
                user.append("Coordinator")
            else:
                user.append("Student")
     
        cursor.close()
        conn.close()
        return self.userList

    def approveOrReject(self, User_id, status):
        conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')
        print("db connected")
        cursor = conn.cursor()
        # if user has been approved
        if status == 1:
            cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, User_id))
            cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, User_id))
            conn.commit()
        elif status == 0:
            cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 0, User_id))
            cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 0, User_id))
            conn.commit()
        cursor.close()
        conn.close()
        return
