import sqlite3
from itertools import chain
from constants import DB_PATH

class Admin:
    def __init__(self):
        self.user_list = []
    
    def open_connection(self):
        try:    
             conn = sqlite3.connect(DB_PATH)
        except Exception as e:
            raise Exception(f"Error has occured connected to the database: {e}")
        return conn
        
    def get_user_list(self, pending_status, approved_status, admin_id):
        try: 
            with self.open_connection() as conn:
                cursor = conn.cursor()
                # gets all users except the admin, prevents deletion
                cursor.execute(''' SELECT User_id, Firstname, Lastname FROM USER_DETAILS WHERE Is_pending = ? AND Is_approved = ? AND User_id != ?''', (pending_status, approved_status, admin_id))
                self.user_list = [list(row) for row in cursor.fetchall()]
            
                for user in self.user_list:
                    # adds all the role of the user to the display for ease for admin
                    cursor.execute(''' SELECT User_id FROM COORDINATORS Where User_id = ?''', (int(user[0]),))
                    if cursor.fetchone():
                        user.append("Coordinator")
                    else:
                        user.append("Student")
        except sqlite3.Error as e:
            raise Exception(f"Error has occured while getting user list: {e}")
        return self.user_list
    
    def individual_approve(self, user_id):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, user_id))
                cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, user_id))
                conn.commit()
        except sqlite3.Error as e:
               raise Exception(f"Error has occured while individually approving users: {e}")
            
    def individual_reject(self, user_id):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('PRAGMA foreign_keys = ON')  # Ensure foreign key constraints are enabled
                cursor.execute('''DELETE FROM USER_DETAILS WHERE User_id = ?''', (user_id,))
                conn.commit() 
        except sqlite3.Error as e:
            # Consider raising custom exceptions or returning error messages
           raise Exception(f"Error has occured while individually deleting users: {e}")

    def mass_approve(self):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ?  WHERE Is_pending = ? AND Is_approved = ?''', (0, 1,1,0))
                cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ?WHERE Is_pending = ? AND Is_approved = ?''', (0, 1,1,0))
                conn.commit()
        except Exception as e:
                raise Exception(f"Error has occured while mass approving users: {e}")
                
                
    def get_user_details(self, user_id):
        try: 
            with self.open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''SELECT * FROM USER_INFORMATION WHERE User_id = ?''', (user_id,))
                user_information = list(chain.from_iterable(cursor.fetchall()))
        except sqlite3.Error as e:
            raise Exception(f"Error has occured while getting user details: {e}")
        return user_information

