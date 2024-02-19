import sqlite3
from constants import DB_PATH


class Verification:

    def isCoord(User_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        identity = cursor.execute('''SELECT User_id FROM COORDINATORS WHERE User_id = ?''', (User_id,))
        id = identity.fetchall()

        if not id:
            print('Student')
            return False
        else:
            print('Coordinator')
            return True

    def isAdmin(User_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        identity = cursor.execute('''SELECT User_id FROM COORDINATORS WHERE User_id = ? AND Coordinator_id = 1''',
                                  (User_id,))
        id = identity.fetchall()

        if not id:
            print('Not admin')
            return False
        else:
            print('Admin')
            return True

    def profileDetails(User_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        details = cursor.execute(
            '''SELECT Firstname, Lastname, Username, Contact_number, Email FROM USER_DETAILS ud INNER JOIN USER_LOGIN ul ON ud.User_id = ul.User_id WHERE ud.User_id = ?''',
            (User_id,))
        profileDetails = []
        for row in details:
            for column in row:
                profileDetails.append(column)
        return profileDetails

    def UserIdToCoordId(User_id):
        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        coordId = cursor.execute('''SELECT Coordinator_id FROM COORDINATORS WHERE User_id = ?''', (User_id,))
        TCoordId = coordId.fetchone()
        for row in TCoordId:
            coordId = row
        conn.close()
        return coordId

    def coordinatingClub(cls, User_id):
        coordId = Verification.UserIdToCoordId(User_id)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        coordinatingClubs = cursor.execute('''SELECT Club_name FROM CLUBS WHERE Coordinator_id = ?''', (coordId,))
        coordinatingClub = coordinatingClubs.fetchone()
        if not coordinatingClub:
            return 'No existing club'
        else:
            for club in coordinatingClub:
                return club


    def clubMemberships(User_id):   #needs to be tested when clubs are added
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        details = cursor.execute(
            '''SELECT Club_name FROM CLUB_MEMBERSHIP cm INNER JOIN CLUBS c ON cm.Club_id = c.Club_id WHERE cm.User_id = ?''',
            (User_id,))
        clubMembership = []
        for row in details:
            for club in row:
                clubMembership.append(club)

        if not clubMembership:
            return None 
        else:
            return clubMembership
        

    def CoordinatorClubId(User_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute('''SELECT Coordinator_id FROM COORDINATORS WHERE User_id = ?''', (User_id,))
            result = cursor.fetchone()

            if result:
                Coordinator_id = result[0]
                cursor.execute('''SELECT Club_id FROM CLUBS WHERE Coordinator_id = ?''', (Coordinator_id,))
                Club_id = cursor.fetchone()
                if Club_id:
                    return Club_id[0]
                else:
                    return "Not associated with any clubs"
            else:
                return None
        finally:
            conn.close()


