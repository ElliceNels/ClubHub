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
