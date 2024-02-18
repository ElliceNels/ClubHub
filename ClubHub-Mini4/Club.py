import sqlite3
from Verification import Verification
from Coordinator import Coordinator
import os
from constants import DB_PATH


class ClubCreationVerification:

    #checks if the user id is associated with a coordinator id
    def valid_coordinator(user_id, coordinator_id):

        try: 
    
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute(''' SELECT Coordinator_id FROM COORDINATORS WHERE User_id = ? ''', (user_id,))
                user_id_verification = cur.fetchone()

                if user_id_verification and user_id_verification[0] == coordinator_id:
                    print("verified user id with coordinator id")
                    return True
                
                else:
                    print("cannot verify user id with coordinator id")
                    return False
                
        except sqlite3.Error as e:
            print("error: ", e)


    #function that lets the user creates new clubs 
    def create_new_club( club_name, club_description, user_id):

        try : 

            coordinator_id = Verification.UserIdToCoordId(user_id)

            with sqlite3.connect(DB_PATH) as conn :
                cur = conn.cursor()

                if ClubCreationVerification.valid_coordinator(user_id, coordinator_id):

                    if not ClubCreationVerification.existing_club(user_id):
                        cur.execute(''' INSERT INTO CLUBS (Club_name, Coordinator_id, Description)
                                    VALUES ( ?, ?, ? ) ''', (club_name, coordinator_id, club_description,))
                        
                        conn.commit()
                        print("data entered successfully")

        except sqlite3.Error as e:
            print("error: ", e)
            
    
    #checks if the user already has a club
    def existing_club(user_id):

        try: 

            coordinator_id = Verification.UserIdToCoordId(user_id)

            with sqlite3.connect(DB_PATH) as conn :
                cur = conn.cursor()

                cur.execute(''' SELECT Coordinator_id, Is_valid FROM CLUBS WHERE Coordinator_id = ? ''', (coordinator_id,))
                coordinator_id_verify = cur.fetchone()

                if coordinator_id_verify and (coordinator_id_verify[1] == 1):
                    print('true')
                    return True
                
                else:
                    print('false')
                    return False


        except sqlite3.Error as e:
            print("error: ", e)
    
# ClubCreationVerification.existing_club(412004)

class ClubDeletion:
    

    def deleteClub(club_name):

        try: 
            club_id = Coordinator.club_getter(club_name)

            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute( ''' PRAGMA foreign_keys = ON ''')
                cur.execute(''' DELETE FROM CLUBS WHERE Club_id = ? ''', (club_id,))
                conn.commit()


        except sqlite3.Error as e:
            print('error: ', e)
