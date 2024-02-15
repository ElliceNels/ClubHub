import sqlite3
from itertools import chain

class Admin:
    def __init__(self):
        self.userList = []
        
    def getUserList(self, pendingstatus, approvedstatus):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("db connected")
        cursor.execute(''' SELECT User_id, Firstname, Lastname FROM USER_DETAILS WHERE Is_pending = ? AND Is_approved = ? AND User_id != ?''', (pendingstatus, approvedstatus, 4121234))
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

    def individualapproveOrReject(self, User_id, status):
        conn = sqlite3.connect(DB_PATH)
        print("db connected")
        cursor = conn.cursor()
        # if user has been approved
        if status == 1:
            try:
                with conn:
                    cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, User_id))
                    cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, User_id))
                    conn.commit()
            except Exception as e:
                print(f"for the developer: Error: {e}")
        elif status == 0:
            try:
                with conn:
                    cursor.execute('PRAGMA foreign_keys = ON')
                    conn.commit()
                    cursor.execute('''DELETE FROM USER_DETAILS WHERE User_id = ?''', (User_id,))
                    conn.commit()
                    print("Deleted from details table")
            
            except Exception as e:
                   print(f"for the developer: Error: {e}")
            finally:
                cursor.close()
                conn.close()
        return
    
    def massapprove(self, status):
        conn = sqlite3.connect(DB_PATH)
        print("db connected")
        cursor = conn.cursor()
        
        if status == 3:
            try:
                with conn:
                    cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ?  WHERE Is_pending = ? AND Is_approved = ?''', (0, 1,1,0))
                    cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ?WHERE Is_pending = ? AND Is_approved = ?''', (0, 1,1,0))
                    conn.commit()
            except Exception as e:
                 print(f"for the developer: Error: {e}")
            finally:
                cursor.close()
                conn.close()
                
                
    def getUserDetails(self, User_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''SELECT ud.user_id, ud.firstname, ud.lastname, ul.username, ud.email,contact_number
        FROM USER_DETAILS as ud
        INNER JOIN USER_LOGIN as ul
        ON ud.User_id = ul.User_id
        WHERE ud.User_id = ?;''', (User_id,))
        userinformation = list(chain.from_iterable(cursor.fetchall()))
        cursor.close()
        conn.close()
        return userinformation

