import sqlite3
from itertools import chain
import bcrypt
from constants import DB_PATH


class LoginVerification:
    def __init__(self):
        self.alert = []

    def userIdExists(self, conn, User_id):
        cursor = conn.cursor()
        cursor.execute(''' SELECT User_id FROM USER_DETAILS Where User_id = ?''', (User_id,))
        ## check if the cursor is empty or not
        # if it is not empty
        if cursor.fetchone():
            cursor.close()
            return True
        cursor.close()
        
    def usernameExists(self, conn, Username):
        cursor = conn.cursor()
        cursor.execute(''' SELECT Username FROM USER_LOGIN Where Username = ?''', (Username,))
        if cursor.fetchone():
            cursor.close()
            return True
        cursor.close()
        
    def emailExists(self, conn, Email):
        cursor = conn.cursor()
        cursor.execute(''' SELECT Email FROM USER_DETAILS Where Email = ?''', (Email,))
        if cursor.fetchone():
            cursor.close()
            return True
        cursor.close()
            
    def insertLoginAndDetails(self, conn, User_id, Username, phonenumber, Password, Firstname, Lastname, Email):
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute(''' INSERT INTO USER_DETAILS (User_id, Firstname, Lastname, Contact_number, Email) VALUES (?, ?, ?, ?, ?)''', (User_id, Firstname, Lastname, phonenumber, Email))
                conn.commit()
                cursor.execute(''' INSERT INTO USER_LOGIN (User_id, Username, Password) VALUES(?, ?, ?)''', (User_id, Username, bcrypt.hashpw(Password.encode(), bcrypt.gensalt())))
                conn.commit()
                cursor.execute(''' SELECT Login_id FROM USER_LOGIN Where User_id = ? ''', (User_id,))
                pendingValue = cursor.fetchone()
                if pendingValue and int((pendingValue)[0]) == 1:
                    cursor.execute(''' UPDATE USER_LOGIN SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, User_id))
                    cursor.execute(''' UPDATE USER_DETAILS SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''', (0, 1, User_id))
                    conn.commit()
        except Exception as e:
            print(f"for the developer: Error: {e}")
            print("for the user: sorry there was an error creating your account")
        finally:
            cursor.close()
            
    def insertCoordinator(self, conn, User_id):
        cursor = conn.cursor()
        try:
            with conn:
                cursor.execute(''' INSERT INTO COORDINATORS (User_id) VALUES (?)''', (User_id,))
                conn.commit()
        except Exception as e:
            print(f"for the developer: Error: {e}")
            print("for the user: sorry there was an error adding you to the coordinator log")
        finally:
            cursor.close()
            
            
    def userdIDUsernamePairExists(self, conn, User_id, Username):
        cursor = conn.cursor()
        cursor.execute(''' SELECT Username FROM USER_LOGIN WHERE User_id = ? AND Username = ? ''', (User_id, Username))
        if cursor.fetchone():
            cursor.close()
            return True
        cursor.close()

    def passwordVerification(self, conn, User_id, Username, Password):
        cursor = conn.cursor()
        cursor.execute(''' SELECT Password FROM USER_LOGIN WHERE User_id = ? AND Username = ?''', (User_id, Username))
        hashedPassword = cursor.fetchone()
        if hashedPassword:
            cursor.close()
            return bcrypt.checkpw(Password.encode(), hashedPassword[0])
        cursor.close()


    def SignUp(self, User_id, Username, Phonenumber, Password, Firstname, Lastname, Email, Usertype):
        # Establish connection
        conn = sqlite3.connect(DB_PATH)
        

        if self.userIdExists(conn, User_id):
            self.alert.append("User_id already exists")
            conn.close()
            return
        else:
            if self.usernameExists(conn, Username):
                self.alert.append('Username already exists')
                conn.close()
                return
            else:
                if self.emailExists(conn, Email):
                    self.alert.append('Email Already exists')
                    conn.close()
                    return 
                else:
                    # if all details are new
                    self.insertLoginAndDetails(conn, User_id, Username, Phonenumber, Password,Firstname, Lastname, Email )
                    if Usertype == 'Coordinator':
                        self.insertCoordinator(conn, User_id)
                    conn.close()
                    return True
        

    def Login(self, User_id, Username, Password):
        conn = sqlite3.connect(DB_PATH)
        # check if an account with the user_id exists
        if self.userIdExists(conn, User_id):
            # check if an account with the user_id and username
            if self.userdIDUsernamePairExists(conn, User_id, Username):
                # check if an account with the user_id, username and password exist
                if self.passwordVerification(conn, User_id, Username, Password):
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
    def approvalStatus(self, User_id):
          conn = sqlite3.connect(DB_PATH)
          cursor = conn.cursor()
          cursor.execute(''' SELECT Is_pending, Is_approved FROM USER_LOGIN WHERE User_id = ?  ''', (User_id,))
          statuses = list(chain.from_iterable(cursor.fetchall()))
          if statuses[0] == 1 and statuses[1] == 0:
              return "Pending"
          elif statuses[0] == 0 and statuses[1] == 0:
              return "Rejected"
          else: 
              return True
