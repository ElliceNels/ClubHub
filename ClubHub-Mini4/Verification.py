import sqlite3



class Verification:

    def isCoord(User_id):
        conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')
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
        conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')
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
        conn = sqlite3.connect('database/Clubhub.db')
        cursor = conn.cursor()

        details = cursor.execute(
            '''SELECT Firstname, Lastname, Username, Contact_number, Email FROM USER_DETAILS ud INNER JOIN USER_LOGIN ul ON ud.User_id = ul.User_id WHERE ud.User_id = ?''',
            (User_id,))
        profileDetails = []
        for row in details:
            for column in row:
                profileDetails.append(column)
        return profileDetails

    User_id = 4121234

    def UserIdToCoordId(User_id):
        conn = sqlite3.connect('database/Clubhub.db')
        cursor = conn.cursor()

        coordId = cursor.execute('''SELECT Coordinator_id FROM COORDINATORS WHERE User_id = ?''', (User_id,))
        coordids = coordId.fetchone()
        print(coordids)
        conn.close()
        return coordids

    def coordinatingClub(self, User_id):
        coordId = self.UserIdToCoordId(self, User_id)
        print(coordId)
        conn = sqlite3.connect('database/Clubhub.db')
        cursor = conn.cursor()

        coordinatingClub = cursor.execute('''SELECT Club_name FROM CLUBS WHERE Coordinator_id = ?''', (coordId,))
        coordinatingClubs = coordinatingClub.fetchone()
        return coordinatingClubs



    profileDetails(4121234)
    UserIdToCoordId(User_id)
    coordinatingClub(User_id)


