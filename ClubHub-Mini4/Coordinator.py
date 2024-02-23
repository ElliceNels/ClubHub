import sqlite3
from Verification import Verification

from constants import DB_PATH

class Coordinator:

    #gets club data to display on the html page
    def get_club_data():

        #initialize an empty club list
        club_details = []

        try:

            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute('''SELECT Club_name, Coordinator_id, Description, Is_valid FROM CLUBS ''')
                club_data = cur.fetchall()
                for row in club_data:
                    club_name = row[0]
                    coord_id = row[1]
                    club_description = row[2]
                    is_valid = row[3]
                    coord_name = Coordinator.coord_name_getter(coord_id)

                    #checks if club is currently active before adding to the list
                    if is_valid == 1:
                        club_details.append([club_name, club_description, coord_name])

            return club_details
        
        except sqlite3.Error as e:
            raise ValueError(f"Error retrieving club details: {e}")


    #gets the coordinator name from their coordinator id
    def coord_name_getter(coord_id):
        try:

            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute(''' SELECT User_id FROM COORDINATORS WHERE Coordinator_id = ? ''', (coord_id,))
                user_id = cur.fetchone()

                cur.execute(''' SELECT Firstname, Lastname, Contact_number FROM USER_DETAILS WHERE User_id = ? ''',(user_id[0],))
                name = cur.fetchone()

                #concatenates the first and last name into full name
                full_name = f"{name[0]} {name[1]}"

                return full_name

        except sqlite3.Error as e:
            raise ValueError(f"Error retrieving coord name: {e}")

    def club_getter(club_name):
        try:

            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute(''' SELECT Club_id FROM CLUBS WHERE Club_name = ? ''', (club_name,))
                club_id = cur.fetchone()
                if club_id is not None:
                    return club_id[0]
            
                else:
                    print(f"No matching record found for club: {club_name}")
                    return None

        except sqlite3.Error as e:
            raise ValueError(f"Error retrieving club: {e}")


    def request_club_membership(user_id, club_name):
        try:

            club_id = Coordinator.club_getter(club_name)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute(''' INSERT INTO CLUB_MEMBERSHIP (User_id, Club_id) VALUES ( ?, ? )''', (user_id, club_id,))
                conn.commit()
                print("data entered successfully")

        except sqlite3.Error as e:
            raise ValueError(f"Error requesting membership: {e}")

    def check_club_requests(user_id, club_name):
        try: 
            
            club_requests = []
            club_id = Coordinator.club_getter(club_name)
            with sqlite3.connect(DB_PATH) as conn :
                cur = conn.cursor()

                cur.execute(''' SELECT Club_id FROM CLUB_MEMBERSHIP WHERE User_id = ? ''', (user_id,))
                club_requests = cur.fetchone()

                if club_requests is not None and (len(club_requests) >= 3 or (club_requests[0] == club_id) or not Verification.isCoord(user_id)):
                    print('true')
                    return True
                
                else:
                    print('false')
                    return False


        except sqlite3.Error as e:
            raise ValueError(f"Error checking membership: {e}")

    
    def display_members(club):
        club_id = Coordinator.club_getter(club)

        try:
            with sqlite3.connect(DB_PATH) as conn :
                cur = conn.cursor()
            cur.execute(''' SELECT User_id FROM CLUB_MEMBERSHIP WHERE Club_id = ? AND Is_approved = 1''' , (club_id,))
            member_ids = cur.fetchall()
            member_details = [Verification.profileDetails(member_id[0]) for member_id in member_ids]
            print(member_ids)
            for members in member_details:
                for member_id in member_ids:
                    print(members)
                    members.append(member_id[0])
            return member_details

        except sqlite3.Error as e:
            raise ValueError(f"Error retrieving members: {e}")

def display_club_events(club_name):
    club_id = Coordinator.club_getter(club_name)
    try:
        with sqlite3.connect(DB_PATH) as conn:
            cur = conn.cursor()
            cur.execute(''' SELECT EventTitle FROM EVENTS WHERE club_id = ?  ''', (club_id,))
            events = cur.fetchone()[0]
            print(events)
            return events
    
    except sqlite3.Error as e:
        raise ValueError(f"error displaying events: {e}")


display_club_events('rap battles')