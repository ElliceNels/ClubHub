import sqlite3
from Verification import Verification

from constants import DB_PATH
# conn = sqlite3.connect(DB_PATH)
# cur = conn.cursor()

# club_data = cur.execute('''SELECT Club_name,Coordinator_id, Description FROM CLUBS ''')

# user_data = cur.execute(''' SELECT Firstname, Lastname, Contact_number FROM USER_DETAILS ''')

# for row in user_data:
#     print(row)

# for row in club_data:
#     for column in row:
#         coordinator_name = cur.execute(''' SELECT Firstname, Lastname, Contact_number FROM USER_DETAILS WHERE User_id = ? ''', (column[1],))
#         print(coordinator_name)


# cur.close()
# conn.close()


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
            print('error: ', e)


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
            print('error: ', e)

    def club_getter(club_name):
        try:

            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute(''' SELECT Club_id FROM CLUBS WHERE Club_name = ? ''', (club_name,))
                club_id = cur.fetchone()
                print(club_id[0])

                return club_id[0]

        except sqlite3.Error as e:
            print('error: ', e)


    def request_club_membership(user_id, club_name):
        try:

            club_id = Coordinator.club_getter(club_name)
            with sqlite3.connect(DB_PATH) as conn:
                cur = conn.cursor()

                cur.execute(''' INSERT INTO CLUB_MEMBERSHIP (User_id, Club_id) VALUES ( ?, ? )''', (user_id, club_id,))
                conn.commit()
                print("data entered successfully")

        except sqlite3.Error as e:
            print("error: ", e)

    def check_club_requests(user_id, club_name):
        try: 
            
            club_requests = []
            club_id = Coordinator.club_getter(club_name)
            with sqlite3.connect(DB_PATH) as conn :
                cur = conn.cursor()

                cur.execute(''' SELECT Club_id FROM CLUB_MEMBERSHIP WHERE User_id = ? ''', (user_id,))
                club_requests = cur.fetchone()

                if club_requests is not None and (len(club_requests) >=3 or (club_requests[0] == club_id)):
                    print('true')
                    return True
                
                else:
                    print('false')
                    return False


        except sqlite3.Error as e:
            print("error: ", e)

    
    def display_members(club):
        club_id = Coordinator.club_getter(club)

        try:
            with sqlite3.connect('ClubHub-Mini4\database\Clubhub.db') as conn :
                cur = conn.cursor()
            cur.execute(''' SELECT User_id FROM CLUB_MEMBERSHIP WHERE Club_id = ? ''', (club_id,))
            members = cur.fetchone()
            member_details = Verification.profileDetails(members[0])
            print(members[0])
            print(member_details)


        except sqlite3.Error as e:
            print("error: ", e )


