import sqlite3
from itertools import chain
import bcrypt
from constants import DB_PATH


class Login_verification:
    def __init__(self):
        self.alert = []

    def user_id_exists(self, conn, user_id):
        cursor = conn.cursor()
        cursor.execute(''' SELECT User_id FROM USER_DETAILS Where User_id = ?''', (user_id,))
        ## check if the cursor is empty or not
        # if it is not empty
        if cursor.fetchone():
            cursor.close()
            return True
        cursor.close()
        
    def username_exists(self, conn, user_name):
        cursor = conn.cursor()
        cursor.execute(''' SELECT Username FROM USER_LOGIN Where Username = ?''', (user_name,))
        if cursor.fetchone():
            cursor.close()
            return True
        cursor.close()
        
    def email_exists(self, conn, email):
        cursor = conn.cursor()
        cursor.execute(''' SELECT Email FROM USER_DETAILS Where Email = ?''', (email,))
        if cursor.fetchone():
            cursor.close()
            return True
        cursor.close()
            
    def insert_login_and_details(self, conn, user_id, user_name, phone_number, password, first_name, last_name, email):
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute(''' INSERT INTO USER_DETAILS (User_id, Firstname, Lastname, Contact_number, Email) VALUES (?, ?, ?, ?, ?)''', (user_id, first_name, last_name, phone_number, email))
                conn.commit()
                cursor.execute(''' INSERT INTO USER_LOGIN (User_id, Username, Password) VALUES(?, ?, ?)''', (user_id, user_name, bcrypt.hashpw(password.encode(), bcrypt.gensalt())))
                conn.commit()
                cursor.execute(''' SELECT Login_id FROM USER_LOGIN Where User_id = ? ''', (user_id,))
                pendingValue = cursor.fetchone()
                if pendingValue and int((pendingValue)[0]) == 1:
                    cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, user_id))
                    cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, user_id))
                    conn.commit()
        except Exception as e:
            print(f"for the developer: Error: {e}")
            print("for the user: sorry there was an error creating your account")
        finally:
            cursor.close()
            
    def insert_coordinator(self, conn, user_id):
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute(''' INSERT INTO COORDINATORS (User_id) VALUES (?)''', (user_id,))
                conn.commit()
        except Exception as e:
            print(f"for the developer: Error: {e}")
            print("for the user: sorry there was an error adding you to the coordinator log")
        finally:
            cursor.close()
            
            
    def user_id_username_pair_exists(self, conn, user_id, user_name):
        cursor = conn.cursor()
        cursor.execute(''' SELECT Username FROM USER_LOGIN WHERE User_id = ? AND Username = ? ''', (user_id, user_name))
        if cursor.fetchone():
            cursor.close()
            return True
        cursor.close()

    def password_verification(self, conn, user_id, user_name, password):
        cursor = conn.cursor()
        cursor.execute(''' SELECT Password FROM USER_LOGIN WHERE User_id = ? AND Username = ?''', (user_id, user_name))
        hashed_password = cursor.fetchone()
        if hashed_password:
            cursor.close()
            return bcrypt.checkpw(password.encode(), hashed_password[0])
        cursor.close()


    def Sign_up(self, user_id, user_name, phone_number, password, first_name, last_name, email, user_type):
        # Establish connection
        print("sign up has been reached")
        conn = sqlite3.connect(DB_PATH)
        

        if self.user_id_exists(conn, user_id):
            self.alert.append("User_id already exists")
            conn.close()
            return
        else:
            if self.username_exists(conn, user_name):
                self.alert.append('Username already exists')
                conn.close()
                return
            else:
                if self.email_exists(conn, email):
                    self.alert.append('Email Already exists')
                    conn.close()
                    return 
                else:
                    # if all details are new
                    self.insert_login_and_details(conn, user_id, user_name, phone_number, password,first_name, last_name, email )
                    if user_type == 'Coordinator':
                        self.insert_coordinator(conn, user_id)
                    conn.close()
                    return True
        

    def Login(self, user_id, user_name, password):
        conn = sqlite3.connect(DB_PATH)
        # check if an account with the user_id exists
        if self.user_id_exists(conn, user_id):
            # check if an account with the user_id and username
            if self.user_id_username_pair_exists(conn, user_id, user_name):
                # check if an account with the user_id, username and password exist
                if self.password_verification(conn, user_id, user_name, password):
                    conn.close()
                    return True
                    #rest of login logic
                else:
                    self.alert.append('incorrect password')
            else:
                self.alert.append('incorrect username')     
        else:
            self.alert.append('no account with this User id exists')
        conn.close()
        return
    
    def get_user_id_from_username(self, user_name):
        conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')
        cursor = conn.cursor()
        cursor.execute(''' SELECT User_id FROM USER_LOGIN WHERE Username = ? ''', (user_name, ))
        user_id_list = list(chain.from_iterable(cursor.fetchall()))
        user_id = int(user_id_list[0])
        cursor.close()
        conn.close()
        return user_id
    
    def approval_status(self, User_id):
          conn = sqlite3.connect(DB_PATH)
          cursor = conn.cursor()
          cursor.execute(''' SELECT Is_pending, Is_approved FROM USER_LOGIN WHERE User_id = ?  ''', (User_id,))
          statuses = list(chain.from_iterable(cursor.fetchall()))
          if statuses[0] == 1 and statuses[1] == 0:
              return "Pending"
          else: 
              return True
