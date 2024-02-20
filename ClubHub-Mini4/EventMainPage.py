import datetime
from constants import DB_PATH
import sqlite3


def eventsmainpage():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('SELECT EventTitle, EventTime, Description, EventDate , Event_id FROM EVENTS')
    eventsmainpage = cursor.fetchall()

#coverting date strings to date objects since its being retrived as a string 
    eventsmainpage = [(title, time, description, datetime.datetime.strptime(date_str, '%Y-%m-%d').date().strftime('%a, %b %d'), event_id) for title, time,description ,date_str, event_id in eventsmainpage]
    
    eventsmainpage.sort(key=lambda x: datetime.datetime.strptime(x[3], '%a, %b %d').date())
    #this sorts events in ascending order based on the third item which is the date, key function extracts the date from each tuple
#lambda creates an anoynmous function
    #date string is being turned into a datetime object to parse the string - makes it easier to sort 
    
    cursor.close()
    connection.close()

    return eventsmainpage

def eventDetails(event_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('SELECT e.EventTitle, e.EventTime, e.Description, e.EventDate, e.Venue, e.Club_id, c.Club_name FROM Events e LEFT JOIN CLUBS c ON e.Club_id = c.Club_id WHERE Event_id = ?', (event_id,))
    #this get the event title, description,venue ,date , time from events table , joins to club table using the club id to get club name
    eventDetails = cursor.fetchall()


    eventDetails = [(title, time, description, datetime.datetime.strptime(date_str, '%Y-%m-%d').date().strftime('%a, %b %d'), venue, club_id ,club_name) for title, time, description, date_str, venue, club_id, club_name in eventDetails]
    if len(eventDetails) > 0 and len(eventDetails[0]) > 4:
        Club_id = eventDetails[0][4]  # Assuming Club ID is at index 4
    else:
        Club_id = None
    cursor.close()
    connection.close()

    club_info(Club_id)
    return eventDetails  

def club_info(Club_id):

    if Club_id is not None:
     
        connection = sqlite3.connect(DB_PATH)
        cursor = connection.cursor()
        cursor.execute('SELECT Club_name, Description, Created FROM CLUBS WHERE Club_id = ?', (Club_id,))
        club_info = cursor.fetchall()

        
        cursor.close()
        connection.close()
        print("Club Info:", club_info)
        return club_info
    else:
        print("Noclub id found")
        return None
    
def userClub():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('SELECT ')