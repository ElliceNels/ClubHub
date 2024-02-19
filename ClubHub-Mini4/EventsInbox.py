import sqlite3
from Verification import Verification
from ClubInbox import ClubInbox
from constants import DB_PATH


class EventsInbox:

    def __init__(self):
        self.eventList = None
        self.waitingList = []

    def CoordIDtoEventsID(self, CoordId):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        print("Coord ID To Event ID:", CoordId, )
        ClubId = ClubInbox.CoordIDtoClubID(ClubInbox, CoordId)
        EventId = cursor.execute('''SELECT Event_id FROM EVENTS WHERE Club_id = ?''', (ClubId,))

        Events = EventId.fetchall()

        ids = []
        for e in Events:
            ids.append(e[0])

        return ids

    def isMemberOfClub(User_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        cursor.execute('''SELECT * FROM CLUB_MEMBERSHIP WHERE User_id = ?''', (User_id,))
        if cursor.fetchall():
            return True
        else:
            return False

    def getEventWaitList(self, User_id, pendingstatus):
        conn = sqlite3.connect(DB_PATH)

        cursor = conn.cursor()

        # cursor.execute('''INSERT INTO CLUB_MEMBERSHIP (User_id, Club_id) VALUES(?,?)''', (4121234, 3))
        # conn.commit()
        CoordID = Verification.UserIdToCoordId(User_id)
        Events = self.CoordIDtoEventsID(CoordID)

        print('Coordid', CoordID)
        print('event id', Events)
        ids = ", ".join([str(id) for id in Events])
        print(ids)

        data = cursor.execute(
            f''' SELECT ea.User_id, Firstname, Lastname FROM EVENT_ATTENDEES ea INNER JOIN USER_DETAILS ud ON ea.User_id = ud.User_id WHERE ea.Is_pending = ? AND ea.Event_id IN ({ids})''',
            (pendingstatus,))
        allData = data.fetchall()

        for entries in allData:

            if self.isMemberOfClub(entries[0]):
                print('is a member, auto accept')
                self.individualapproveOrRejectE(entries[0], 1)
            else:
                print('not member, waiting verification')
                self.eventList = [list(row) for row in allData]
                print(self.eventList)
                for user in self.eventList:
                    cursor.execute(''' SELECT User_id FROM COORDINATORS Where User_id = ?''', (int(user[0]),))
                    user.append(user[1] + " would like to come to your event")

        cursor.close()
        conn.close()
        if not self.eventList:
            return ''
        else:
            return self.eventList

    def individualapproveOrRejectE(self, User_id, status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        # if user has been approved
        if status == 1:
            try:
                with conn:
                    cursor.execute(''' UPDATE EVENT_ATTENDEES SET Is_pending = ?, Is_approved = ? WHERE User_id = ?''',
                                   (0, 1, User_id))
                    conn.commit()
            except Exception as e:
                print(f"for the developer: Error: {e}")
        elif status == 0:
            try:
                with conn:
                    cursor.execute('PRAGMA foreign_keys = ON')
                    conn.commit()
                    cursor.execute('''DELETE FROM EVENT_ATTENDEES WHERE User_id = ?''', (User_id,))
                    conn.commit()
                    print("Deleted from details table")

            except Exception as e:
                print(f"for the developer: Error: {e}")
            finally:
                cursor.close()
                conn.close()
        return


    def massapproveE(self, status):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        if status == 3:
            try:
                with conn:
                    cursor.execute(
                        ''' UPDATE EVENT_ATTENDEES SET Is_pending = ?, Is_approved = ?  WHERE Is_pending = ? AND Is_approved = ?''',
                        (0, 1, 1, 0))
                    conn.commit()

            except Exception as e:
                print(f"for the developer: Error: {e}")
            finally:
                cursor.close()
                conn.close()

