from constants import DB_PATH
import sqlite3


def register_events(EventTitle , Description , event_date, event_time, Venue ,Club_id):
        conn = sqlite3.connect(DB_PATH)

        try:
                cursor = conn.cursor() 
#cursor object executes SQL commands
                sql = "INSERT INTO EVENTS( EventTitle, Description, EventDate, EventTime , Venue, Clud_id) VALUES (?, ?, ?, ?, ?, ?)"
                #? are placeholders in sqlite3
                cursor.execute(sql, (EventTitle, Description, event_date, event_time, Venue, Club_id))
                conn.commit()
        finally:
                conn.close()