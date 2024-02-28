import sqlite3
from constants import DB_PATH
from Verification import Verification


class ClubInbox:

    def __init__(self):
        self.event_list = None
        self.user_list = []
        self.waiting_list = []

    def CoordIDtoClubID(self, coord_id):
        try:
            # connection to database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # get club id from coord id
            club_id = cursor.execute('''SELECT Club_id FROM CLUBS WHERE Coordinator_id = ?''', (coord_id,))
            id = club_id.fetchone()
        except sqlite3.Error as e:
            print(f"Error has occured while getting club id: {e}")

        # ensures that this coord has a club else return null
        if id is None:
            return None
        return id[0]

    def clubApprovalList(self, user_id, pending_status):

        # find club id from the coord id
        coord_id = Verification.UserIdToCoordId(user_id)
        club_id = self.CoordIDtoClubID(coord_id)
        print('club id is', club_id)

        try:
            # connection to database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # get details of person pending for club id
            code = cursor.execute(
                ''' SELECT cm.User_id, Firstname, Lastname FROM CLUB_MEMBERSHIP cm INNER JOIN USER_DETAILS ud ON cm.User_id = ud.User_id WHERE cm.Is_pending = ? AND cm.Club_id = ?''',
                (pending_status, club_id))

            # add them to the waiting list
            self.waiting_list = [list(row) for row in code.fetchall()]

            # add description to each person's details
            for user in self.waiting_list:
                user.append(user[1] + " would like to join your club")

            cursor.close()
            conn.close()
        except sqlite3.Error as e:
            print(f"Error has occured when getting club approval list: {e}")

        # return nothing if the waiting list is empty
        if not self.waiting_list:
            return ''
        else:
            return self.waiting_list

    def massapprove(self, status):
        # connection to database
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # when mass approve button is pressed
        if status == 3:
            try:
                with conn:
                    # update all rows to approved and not pending
                    cursor.execute(
                        ''' UPDATE CLUB_MEMBERSHIP SET Is_pending = ?, Is_approved = ?  WHERE Is_pending = ? AND Is_approved = ?''',
                        (0, 1, 1, 0))
                    conn.commit()

            except Exception as e:
                print(f"for the developer: Error: {e}")
            finally:
                cursor.close()
                conn.close()




