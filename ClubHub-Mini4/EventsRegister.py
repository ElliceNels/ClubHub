import sqlite3

def register_events(EventTitle , Description , event_date, event_time, Venue):
        conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')

        try:
                cursor = conn.cursor() 
#cursor object executes SQL commands
                sql = "INSERT INTO EVENTS( EventTitle, Description, EventDate, EventTime , Venue) VALUES (?, ?, ?, ?, ?)"
                #? are placeholders in sqlite3
                cursor.execute(sql, (EventTitle, Description, event_date, event_time, Venue))
                conn.commit()
        finally:
                conn.close()