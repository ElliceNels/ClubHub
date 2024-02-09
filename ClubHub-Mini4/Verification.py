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

        identity = cursor.execute('''SELECT User_id FROM COORDINATORS WHERE User_id = ? AND Coordinator_id = 1''', (User_id,))
        id = identity.fetchall()

        if not id:
            print('Not admin')
            return False
        else:
            print('Admin')
            return True

    def profileDetails(User_id):
        conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')
        cursor = conn.cursor()

        details = cursor.execute('''SELECT Firstname, Lastname, Username, Contact_number, Email FROM USER_DETAILS ud INNER JOIN USER_LOGIN ul ON ud.User_id = ul.User_id WHERE ud.User_id = ?''', (User_id,))
        for row in details:
            for column in row:
              print(column)

    #def findClub(Coordinator_id):
     #   conn = sqlite3.connect('database/Clubhub.db')
      #  cursor = conn.cursor()

       # clubOwned
    profileDetails(4121234)
    isAdmin(4121234)