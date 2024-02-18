import datetime
from constants import DB_PATH
import sqlite3


def eventsmainpage():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('SELECT EventTitle, EventTime, EventDate FROM EVENTS')
    eventsmainpage = cursor.fetchall()

#coverting date strings to date objects since its being retrived as a string 
    eventsmainpage = [(title, time, datetime.datetime.strptime(date_str, '%Y-%m-%d').date().strftime('%a, %b %d')) for title, time, date_str in eventsmainpage]
    
    eventsmainpage.sort(key=lambda x: x[2])
    #this sorts events in ascending order based on the third item which is the date, key function extracts the date from each tuple
#lambda creates an anoynmous function
    
    cursor.close()
    connection.close()

    return eventsmainpage