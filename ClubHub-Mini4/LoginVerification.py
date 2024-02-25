import sqlite3
from itertools import chain
import bcrypt
from constants import DB_PATH


class Login_verification:
    def __init__(self):
        self.alert = []
        
    def open_connection(self):
        conn = sqlite3.connect(DB_PATH)
        return conn
        
    def user_id_exists(self, user_id):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(''' SELECT User_id FROM USER_DETAILS Where User_id = ?''', (user_id,))
                ## check if the cursor is empty or not
                if cursor.fetchone():
                    return True # if it is not empty
        except sqlite3.Error as e:
            raise Exception(f"an error has occured determining if user_id exists: {e}")
    
        
    def username_exists(self, user_name):
        try:
           with self.open_connection() as conn:
                cursor = conn.cursor()
                # checks if there is already an account with that username
                cursor.execute(''' SELECT Username FROM USER_LOGIN Where Username = ?''', (user_name,))
                if cursor.fetchone():
                    return True
        except sqlite3.Error as e:
            raise Exception(f"an error has occured determining if user name exists: {e}")
        
    def email_exists(self, email):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                # checks if there is already an account with that email
                cursor.execute(''' SELECT Email FROM USER_DETAILS Where Email = ?''', (email,))
                if cursor.fetchone():
                    return True
        except sqlite3.Error as e:
           raise Exception(f"an error has occured determining if user name exists: {e}")
            
    def insert_login_and_details(self, user_id, user_name, phone_number, password, first_name, last_name, email):
        conn = sqlite3.connect(DB_PATH)
        try:
            with conn:
                cursor = conn.cursor()
                cursor.execute(''' INSERT INTO USER_DETAILS (User_id, Firstname, Lastname, Contact_number, Email) VALUES (?, ?, ?, ?, ?)''', (user_id, first_name, last_name, phone_number, email))
                conn.commit()
                cursor.execute(''' INSERT INTO USER_LOGIN (User_id, Username, Password) VALUES(?, ?, ?)''', (user_id, user_name, bcrypt.hashpw(password.encode(), bcrypt.gensalt())))
                conn.commit()
                cursor.execute(''' SELECT Login_id FROM USER_LOGIN Where User_id = ? ''', (user_id,))
                pendingValue = cursor.fetchone()
                if pendingValue and int((pendingValue)[0]) == 1:
                    # approves the user to login freely
                    cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, user_id))
                    cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, user_id))
                    conn.commit()
        except Exception as e:
            conn.rollback()
            raise Exception(f"an error has occured inserting details: {e}")
                  
            
    def insert_coordinator(self, user_id):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(''' INSERT INTO COORDINATORS (User_id) VALUES (?)''', (user_id,))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"an error has occured inserting coordinator: {e}")
            
            
    def user_id_username_pair_exists(self, user_id, user_name):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                # checks if there exists the user_id and username combo in the system for logging in
                cursor.execute(''' SELECT Username FROM USER_LOGIN WHERE User_id = ? AND Username = ? ''', (user_id, user_name))
                if cursor.fetchone():
                    return True
        except sqlite3.Error as e:
            raise Exception(f"an error has occured determining if user name pair exists: {e}")

    def password_verification(self, user_id, user_name, password):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                # checks if that is the right password for the account
                cursor.execute(''' SELECT Password FROM USER_LOGIN WHERE User_id = ? AND Username = ?''', (user_id, user_name))
                hashed_password = cursor.fetchone()
                if hashed_password:
                    return bcrypt.checkpw(password.encode(), hashed_password[0])
        except Exception as e:
            raise Exception(f"an error has occured signing up: {e}")


    def Sign_up(self, user_id, user_name, phone_number, password, first_name, last_name, email, user_type):
        # Establish connection
        try: 
            with self.open_connection() as conn:
                if self.user_id_exists( user_id):
                    self.alert.append("User_id already exists")
                    return
                else:
                    if self.username_exists(user_name):
                        self.alert.append('Username already exists')
                        return
                    else:
                        if self.email_exists(email):
                            self.alert.append('Email Already exists')
                            return 
                        else:
                            # if all details are new
                            self.insert_login_and_details(user_id, user_name, phone_number, password,first_name, last_name, email )
                            if user_type == 'Coordinator':
                                self.insert_coordinator(user_id)
                            return True
        except Exception as e:
            conn.rollback()
            raise Exception(f"an error has occured signing up: {e}")
                

    def Login(self, user_id, user_name, password):
        try:
            with self.open_connection() as conn:
                # check if an account with the user_id exists
                if self.user_id_exists(user_id):
                    # check if an account with the user_id and username
                    if self.user_id_username_pair_exists(user_id, user_name):
                        # check if an account with the user_id, username and password exist
                        if self.password_verification(user_id, user_name, password):
                            return True
                            #rest of login logic
                        else:
                            self.alert.append('incorrect password')
                    else:
                        self.alert.append('incorrect username')     
                else:
                    self.alert.append('no account with this User id exists')
                return
        except Exception as e:
            raise Exception(f"an error has occured logging in {e}")
            
    def get_user_id_from_username(self, user_name):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(''' SELECT User_id FROM USER_LOGIN WHERE Username = ? ''', (user_name, ))
                user_id_list = list(chain.from_iterable(cursor.fetchall()))
                if user_id_list != []: # prevents a none error
                    user_id = int(user_id_list[0])
                    return user_id
                return False
        except Exception as e:
            raise Exception(f"an error has occured getting user_id from username {e}")
            
    def approval_status(self, User_id):
        try:
            with self.open_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(''' SELECT Is_pending, Is_approved FROM USER_LOGIN WHERE User_id = ?  ''', (User_id,))
                statuses = list(chain.from_iterable(cursor.fetchall()))
                if statuses[0] == 1 and statuses[1] == 0:
                    return "Pending"
                else: 
                    return True
        except Exception as e:
            raise Exception(f"an error has occured getting the approval status {e}")
            
