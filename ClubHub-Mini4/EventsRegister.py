from constants import DB_PATH
import sqlite3


def register_events(event_title , description , event_date, event_time, venue , club_id ):
        conn = sqlite3.connect(DB_PATH)

        try:
                cursor = conn.cursor() 
#cursor object executes SQL commands
                sql = "INSERT INTO EVENTS(EventTitle, Description, EventDate, EventTime, Venue, Club_id ) VALUES (?, ?, ?, ?, ?, ?)"
                #? are placeholders in sqlite3
                cursor.execute(sql, (event_title, description, event_date, event_time, venue, club_id))
                conn.commit()
        finally:
                conn.close()