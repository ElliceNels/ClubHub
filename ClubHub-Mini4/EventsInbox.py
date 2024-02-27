import sqlite3
from Verification import Verification
from ClubInbox import ClubInbox
from constants import DB_PATH


class EventsInbox:

    def __init__(self):
        self.event_list = None
        self.waiting_list = []

    def CoordIDtoEventsID(self, coord_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()
            print("Coord ID To Event ID:", coord_id, )
            club_id = ClubInbox.CoordIDtoClubID(ClubInbox, coord_id)
            event_id = cursor.execute('''SELECT Event_id FROM EVENTS WHERE Club_id = ?''', (club_id,))

            events = event_id.fetchall()

            ids = []
            for e in events:
                ids.append(e[0])

            return ids
        except sqlite3.Error as e:
            print(f"Error has occurred when getting event id: {e}")

    def isMemberOfClub(self, user_id):
        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            cursor.execute('''SELECT * FROM CLUB_MEMBERSHIP WHERE User_id = ?''', (user_id,))
            if cursor.fetchall():
                return True
            else:
                return False
        except sqlite3.Error as e:
            print(f"Error has occured when checking member status: {e}")

    def getEventWaitList(self, user_id, pending_status):
        coord_id = Verification.UserIdToCoordId(user_id)
        events = self.CoordIDtoEventsID(coord_id)

        print('Coordid', coord_id)
        print('event id', events)
        ids = ", ".join([str(id) for id in events])
        print(ids)

        try:
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            data = cursor.execute(
                f''' SELECT ea.User_id, Firstname, Lastname FROM EVENT_ATTENDEES ea INNER JOIN USER_DETAILS ud ON 
                ea.User_id = ud.User_id WHERE ea.Is_pending = ? AND ea.Event_id IN ({ids})''',
                (pending_status,))
            all_data = data.fetchall()

            for entries in all_data:

                if self.isMemberOfClub(user_id):
                    print('is a member, auto accept')
                else:
                    print('not member, waiting verification')
                    self.event_list = [list(row) for row in all_data]
                    print(self.event_list)
                    for user in self.event_list:
                        cursor.execute(''' SELECT User_id FROM COORDINATORS Where User_id = ?''', (int(user[0]),))
                        user.append(user[1] + " would like to come to your event")

            cursor.close()
            conn.close()
            if not self.event_list:
                return ''
            else:
                return self.event_list
        except sqlite3.Error as e:
            print(f"Error has occurred when getting event waitlist: {e}")

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

