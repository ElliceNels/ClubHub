import sqlite3
from constants import DB_PATH


class Verification:

    def isCoord(user_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        identity = cursor.execute('''SELECT User_id FROM COORDINATORS WHERE User_id = ?''', (user_id,))
        id = identity.fetchall()

        if not id:
            print('Student')
            return False
        else:
            print('Coordinator')
            return True

    def isAdmin(user_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        identity = cursor.execute('''SELECT User_id FROM COORDINATORS WHERE User_id = ? AND Coordinator_id = 1''',
                                  (user_id,))
        id = identity.fetchall()

        if not id:
            print('Not admin')
            return False
        else:
            print('Admin')
            return True

    def profileDetails(user_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        details = cursor.execute(
            '''SELECT Firstname, Lastname, Username, Contact_number, Email FROM USER_DETAILS ud INNER JOIN USER_LOGIN ul ON ud.User_id = ul.User_id WHERE ud.User_id = ?''',
            (user_id,))
        profile_details = []
        for row in details:
            for column in row:
                profile_details.append(column)
        return profile_details

    def UserIdToCoordId(user_id):
        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        coord_id = cursor.execute('''SELECT Coordinator_id FROM COORDINATORS WHERE User_id = ?''', (user_id,))
        t_coord_id = coord_id.fetchone()
        if not t_coord_id:
            return 'not a coord'
        for row in t_coord_id:
            coord_id = row
        conn.close()
        return coord_id

    def coordinatingClub(cls, user_id):
        coord_id = Verification.UserIdToCoordId(user_id)
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        coordinating_clubs = cursor.execute('''SELECT Club_name FROM CLUBS WHERE Coordinator_id = ?''', (coord_id,))
        coordinating_club = coordinating_clubs.fetchone()
        if not coordinating_club:
            return 'No existing club'
        else:
            for club in coordinating_club:
                return club

    def clubMemberships(user_id):  # needs to be tested when clubs are added
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        details = cursor.execute(
            '''SELECT Club_name FROM CLUB_MEMBERSHIP cm INNER JOIN CLUBS c ON cm.Club_id = c.Club_id WHERE cm.User_id = ? AND Is_approved = ?''',
            (user_id, 1))
        club_membership = []
        for row in details:
            for club in row:
                club_membership.append(club)

        if not club_membership:
            return None
        else:
            return club_membership

    def CoordinatorClubId(user_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        try:
            cursor.execute('''SELECT Coordinator_id FROM COORDINATORS WHERE User_id = ?''', (user_id,))
            result = cursor.fetchone()

            if result:
                coordinator_id = result[0]
                cursor.execute('''SELECT Club_id FROM CLUBS WHERE Coordinator_id = ?''', (coordinator_id,))
                club_id = cursor.fetchone()
                if club_id:
                    return club_id[0]
                else:
                    return "Not associated with any clubs"
            else:
                return None
        finally:
            conn.close()


    def individualapproveOrReject(self, user_id, status, table):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # if user has been approved
        if status == 1:
            try:
                with conn:
                    cursor.execute(f''' UPDATE {table} SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''',
                                   (0, 1, user_id))
                    conn.commit()
            except Exception as e:
                print(f"for the developer: Error: {e}")
        elif status == 0:
            try:
                with conn:
                    cursor.execute('PRAGMA foreign_keys = ON')
                    conn.commit()
                    cursor.execute(f'''DELETE FROM {table} WHERE User_id = ?''', (user_id,))
                    conn.commit()
                    print("Deleted from details table")

            except Exception as e:
                print(f"for the developer: Error: {e}")
            finally:
                cursor.close()
                conn.close()
        return
