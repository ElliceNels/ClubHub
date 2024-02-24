import sqlite3
from Verification import Verification
from Coordinator import Coordinator
from constants import DB_PATH

# has all the backend for verifying and creating clubs
class ClubCreationVerification:

    # checks if the user id is associated with a coordinator id
    def valid_coordinator(user_id, coordinator_id):

        try: 
    
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute(''' SELECT Coordinator_id FROM COORDINATORS WHERE User_id = ? ''', (user_id,))
                user_id_verification = cur.fetchone()

                if user_id_verification and user_id_verification[0] == coordinator_id:
                    # verified user id with coordinator id
                    return True
                
                else:
                    # cannot verify user id with coordinator id
                    return False
                
        except sqlite3.Error as e:
            raise ValueError(f"Error retrieving validation: {e}")

    # checks if the club actually exists in the database
    def club_name_checker(club_name):
        try: 
    
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute(''' SELECT Club_name FROM CLUBS WHERE Club_name = ? ''', (club_name,))
                verify = cur.fetchone()

                if verify:
                    # club exists
                    return True
                
                else:
                    # club doesnt exist
                    return False
                
        except sqlite3.Error as e:
            raise ValueError(f"Error retrieving club: {e}")



    # function that lets the user creates new clubs 
    def create_new_club( club_name, club_description, user_id):

        try : 

            #gets coord id from user id
            coordinator_id = Verification.UserIdToCoordId(user_id)

            with sqlite3.connect(DB_PATH) as conn :
                cur = conn.cursor()

                # vefication if coord id and user id are the same user
                if ClubCreationVerification.valid_coordinator(user_id, coordinator_id):

                    if not ClubCreationVerification.existing_club(user_id) and not ClubCreationVerification.club_name_checker(club_name):
                        cur.execute(''' INSERT INTO CLUBS (Club_name, Coordinator_id, Description)
                                    VALUES ( ?, ?, ? ) ''', (club_name, coordinator_id, club_description,))
                        
                        conn.commit()

        except sqlite3.Error as e:
            raise ValueError(f"Error creating club: {e}")
            
    
    #checks if the user already has a club
    def existing_club(user_id):

        try: 

            # gets coord id from user id
            coordinator_id = Verification.UserIdToCoordId(user_id)

            with sqlite3.connect(DB_PATH) as conn :
                cur = conn.cursor()

                cur.execute(''' SELECT Coordinator_id, Is_valid FROM CLUBS WHERE Coordinator_id = ? ''', (coordinator_id,))
                coordinator_id_verify = cur.fetchone()

                # if they already have a club return true
                if coordinator_id_verify and (coordinator_id_verify[1] == 1):
                    return True
                
                else:
                    return False


        except sqlite3.Error as e:
            raise ValueError(f"Error retrieving club: {e}")
    

# class for handeling the deletion of clubs
class ClubDeletion:
    
    # function to delete club
    def deleteClub(club_name):

        try: 

            # get club id with club name
            club_id = Coordinator.club_getter(club_name)


            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute( ''' PRAGMA foreign_keys = ON ''')
                cur.execute(''' DELETE FROM CLUBS WHERE Club_id = ? ''', (club_id,))
                
                conn.commit()


        except sqlite3.Error as e:
            raise ValueError(f"Error deleting club: {e}")
