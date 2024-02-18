import sqlite3
from itertools import chain
from constants import DB_PATH

class Admin:
    def __init__(self):
        self.user_list = []
        
    def get_user_list(self, pending_status, approved_status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute(''' SELECT User_id, Firstname, Lastname FROM USER_DETAILS WHERE Is_pending = ? AND Is_approved = ? AND User_id != ?''', (pending_status, approved_status, 4121234))
        self.user_list = [list(row) for row in cursor.fetchall()]
       
        for user in self.user_list:
            cursor.execute(''' SELECT User_id FROM COORDINATORS Where User_id = ?''', (int(user[0]),))
            if cursor.fetchone():
                user.append("Coordinator")
            else:
                user.append("Student")
     
        cursor.close()
        conn.close()
        return self.user_list
    
    def individual_approve(self, user_id):
        conn = sqlite3.connect(DB_PATH)
        print("db connected")
        cursor = conn.cursor()
        try:
                with conn:
                    cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, user_id))
                    cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, user_id))
                    conn.commit()
        except Exception as e:
                print(f"for the developer: Error: {e}")
        finally:
            cursor.close()
            conn.close()
            
    def individual_reject(self, user_id):
        conn = sqlite3.connect(DB_PATH)
        print("db connected")
        print(F"User_id is {user_id}")
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute('PRAGMA foreign_keys = ON')  # Ensure foreign key constraints are enabled
                cursor.execute('''DELETE FROM USER_DETAILS WHERE User_id = ?''', (user_id,))
                conn.commit() 
        except sqlite3.Error as e:
            # Consider raising custom exceptions or returning error messages
            print(f"Error deleting user details: {e}")
        finally:
            cursor.close()
            conn.close()

    def mass_approve(self, status):
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
                
                
    def get_user_details(self, user_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        cursor.execute('''SELECT * FROM USER_INFORMATION WHERE User_id = ?''', (user_id,))
        userinformation = list(chain.from_iterable(cursor.fetchall()))
        cursor.close()
        conn.close()
        return userinformation

