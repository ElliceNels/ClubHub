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
            # connection to database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # get club id from coord id then get the event ids
            club_id = ClubInbox.CoordIDtoClubID(ClubInbox, coord_id)
            event_id = cursor.execute('''SELECT Event_id FROM EVENTS WHERE Club_id = ?''', (club_id,))

            # events - all events of this club
            events = event_id.fetchall()

            # tidy list version of the event ids
            ids = []
            for e in events:
                ids.append(e[0])

            return ids
        except sqlite3.Error as e:
            print(f"Error has occurred when getting event id: {e}")

    def getEventWaitList(self, user_id, pending_status):
        # get event ids from user id
        coord_id = Verification.UserIdToCoordId(user_id)
        events = self.CoordIDtoEventsID(coord_id)

        ids = ", ".join([str(id) for id in events])

        try:
            # connection to database
            conn = sqlite3.connect(DB_PATH)
            cursor = conn.cursor()

            # get details of people in event attendees who arent approved
            data = cursor.execute(
                f''' SELECT ea.User_id, Firstname, Lastname FROM EVENT_ATTENDEES ea INNER JOIN USER_DETAILS ud ON 
                ea.User_id = ud.User_id WHERE ea.Is_pending = ? AND ea.Event_id IN ({ids})''',
                (pending_status,))
            all_data = data.fetchall()

            for entries in all_data:
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
        # connection to database
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

