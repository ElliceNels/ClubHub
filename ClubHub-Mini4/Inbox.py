import sqlite3
from constants import DB_PATH

import self as self

from Verification import Verification


class Inbox:

    def __init__(self):
        self.userList = []
        self.waitingList = []

    def isMemberOfClub(self, User_id):
        conn = sqlite3.connect('database/Clubhub.db')
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM CLUB_MEMBERSHIP WHERE User_id = ?''', (User_id,))
        if cursor.fetchall():
            return True
        else:
            return False


    def CoordIDtoClubID(CoordId):
        conn = sqlite3.connect(DB_PATH)
        
        cursor = conn.cursor()
        EventId = cursor.execute('''SELECT Event_id FROM EVENTS WHERE Club_id = ?''', (ClubId,))

        Events = EventId.fetchall()
        return Events

    def CoordIDtoClubID(self, CoordId):
        conn = sqlite3.connect('database/Clubhub.db')
        cursor = conn.cursor()

        ClubId = cursor.execute('''SELECT Club_id FROM CLUBS WHERE Coordinator_id = ?''', (CoordId,))
        id = ClubId.fetchone()
        for iD in id:
            print('CoordId is', CoordId, 'and clubId is', iD)
        return iD

    def clubApprovalList(self,User_id, pendingstatus):
        conn = sqlite3.connect('database/Clubhub.db')
        cursor = conn.cursor()

        CoordID = Verification.UserIdToCoordId(User_id)
        Club_id = Inbox.CoordIDtoClubID(CoordID)

        cursor.execute(
            ''' SELECT cm.User_id, Firstname, Lastname FROM CLUB_MEMBERSHIP cm INNER JOIN USER_DETAILS ud ON cm.User_id = ud.User_id WHERE cm.Is_pending = ? AND cm.Club_id = ?''',
            (pendingstatus, Club_id))
        self.waitingList = [list(row) for row in cursor.fetchall()]

        for user in self.waitingList:
            cursor.execute(''' SELECT User_id FROM COORDINATORS Where User_id = ?''', (int(user[0]),))
            user.append(user[1] + " would like to join your club")

        cursor.close()
        conn.close()

        return self.waitingList


    def getUserList(self, pendingstatus, approvedstatus):
        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        # cursor.execute('''INSERT INTO CLUB_MEMBERSHIP (User_id, Club_id) VALUES(?,?)''', (4121234, 3))
        # conn.commit()
        CoordID = Verification.UserIdToCoordId(User_id)
        Club_id = self.CoordIDtoClubID(CoordID)
        Events = self.ClubIDtoEventID(Club_id)

        cursor.execute(
            ''' SELECT ea.User_id, Firstname, Lastname FROM EVENT_ATTENDEES ea INNER JOIN USER_DETAILS ud ON ea.User_id = ud.User_id WHERE ea.Is_pending = ? AND ea.Event_id = ?''',
            (pendingstatus, Events))
        self.eventList = [list(row) for row in cursor.fetchall()]
        print(self.eventList)
        for user in self.eventList:
            cursor.execute(''' SELECT User_id FROM COORDINATORS Where User_id = ?''', (int(user[0]),))
            user.append(user[1] + " would like to come to your event")

        cursor.close()
        conn.close()

        return self.eventList


    def individualapproveOrReject(self, User_id, status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # if user has been approved
        if status == 1:
            try:
                with conn:
                    cursor.execute(''' UPDATE CLUB_MEMBERSHIP SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''',
                                   (0, 1, User_id))
                    conn.commit()
            except Exception as e:
                print(f"for the developer: Error: {e}")
        elif status == 0:
            try:
                with conn:
                    cursor.execute('PRAGMA foreign_keys = ON')
                    conn.commit()
                    cursor.execute('''DELETE FROM CLUB_MEMBERSHIP WHERE User_id = ?''', (User_id,))
                    conn.commit()
                    print("Deleted from details table")

            except Exception as e:
                print(f"for the developer: Error: {e}")
            finally:
                cursor.close()
                conn.close()
        return

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

newInbox = Inbox()
newInbox.eventApprovalList(4121234, 1)