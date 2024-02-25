import sqlite3
from constants import DB_PATH
from Verification import Verification


class ClubInbox:

    def __init__(self):
        self.event_list = None
        self.user_list = []
        self.waiting_list = []

    def CoordIDtoClubID(self, coord_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        print("Get Club id for coordinator:", coord_id)
        club_id = cursor.execute('''SELECT Club_id FROM CLUBS WHERE Coordinator_id = ?''', (coord_id,))
        id = club_id.fetchone()

        if id is None:
            return None
        return id[0]

    def clubApprovalList(self, user_id, pending_status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        CoordID = Verification.UserIdToCoordId(user_id)
        club_id = self.CoordIDtoClubID(CoordID)
        print('club id is', club_id)

        code = cursor.execute(
            ''' SELECT cm.User_id, Firstname, Lastname FROM CLUB_MEMBERSHIP cm INNER JOIN USER_DETAILS ud ON cm.User_id = ud.User_id WHERE cm.Is_pending = ? AND cm.Club_id = ?''',
            (pending_status, club_id))
        print(code)
        self.waiting_list = [list(row) for row in code.fetchall()]

        for user in self.waiting_list:
            cursor.execute(''' SELECT User_id FROM COORDINATORS Where User_id = ?''', (int(user[0]),))
            user.append(user[1] + " would like to join your club")

        cursor.close()
        conn.close()

        if not self.waiting_list:
            return ''
        else:
            return self.waiting_list

    def membersList(self, user_id, pending_status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        coord_id = Verification.UserIdToCoordId(user_id)
        club_id = self.CoordIDtoClubID(coord_id)
        print('club id is', club_id)

        code = cursor.execute(
            ''' SELECT cm.User_id, Firstname, Lastname FROM CLUB_MEMBERSHIP cm INNER JOIN USER_DETAILS ud ON cm.User_id = ud.User_id WHERE cm.Is_pending = ? AND cm.Club_id = ?''',
            (pending_status, club_id))
        print(code)
        self.waiting_list = [list(row) for row in code.fetchall()]

        cursor.close()
        conn.close()

        if not self.waiting_list:
            return ''
        else:
            return self.waiting_list

    def massapprove(self, status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if status == 3:
            try:
                with conn:
                    cursor.execute(
                        ''' UPDATE CLUB_MEMBERSHIP SET Is_pending = ?, Is_approved = ?  WHERE Is_pending = ? AND Is_approved = ?''',
                        (0, 1, 1, 0))
                    conn.commit()

            except Exception as e:
                print(f"for the developer: Error: {e}")
            finally:
                cursor.close()
                conn.close()




