import datetime
from constants import DB_PATH
import sqlite3


def eventsmainpage():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    current_date = datetime.datetime.now().date()
    cursor.execute('SELECT EventTitle, EventTime, Description, EventDate , Event_id FROM EVENTS WHERE EventDate >= ?',(current_date,))
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
        Club_id = eventDetails[0][4]  #Club ID is at index 4
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
        #gets club info of the club that hosts the even being displayed
        
        cursor.close()
        connection.close()
        print("Club Info:", club_info)
        return club_info
    else:
        print("Noclub id found")
        return None
    
def eventideasy(url): #gets event id as its the last digit in the url - shorcut 
   try:
       event_id = int(url.split("/")[-1])
       return event_id
   except(ValueError,IndexError):
       return None
   

def signup_event(club_id, user_id, event_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    
    try:
    #checks if user is part of the club that is hosting the event 
        cursor.execute('SELECT COUNT(*) FROM user_club_event WHERE Club_id =? AND User_id = ? AND Event_id = ? And Is_approved = 1', (club_id, user_id, event_id))
        club_mem_count = cursor.fetchone()[0]

        if club_mem_count >0:#if user is part of the club, it then checks if they have already signed up to the event
            cursor.execute('SELECT COUNT(*) FROM EVENT_ATTENDEES WHERE User_id = ? AND Event_id = ?', (user_id, event_id))
            event_attendee = cursor.fetchone()[0]
            if  event_attendee >0:#if the user is part of the club its approves them instantly to the event
                return "You already signed up for this event"
        
            else:
                    cursor.execute('INSERT INTO EVENT_ATTENDEES (User_id, Event_id, Is_approved, Is_pending) VALUES (?, ?, 1, 0)', (user_id, event_id))
                    connection.commit()
                    return "You are signed up for the event. See you there!"
        else:#if the user isnt part of the group, it adds them to the event attend table as pending so the co-ordinator can see whether or not to approve them for the event
                cursor.execute('SELECT COUNT(*) FROM EVENT_ATTENDEES WHERE User_id = ? AND Event_id = ? AND Is_pending = 1', (user_id, event_id))
                already_pending = cursor.fetchone()[0]

                if already_pending >0:
                    return "You have already requested to sign up to this event and your status is currently pending"
                else:
                    cursor.execute('INSERT INTO EVENT_ATTENDEES (User_id, Event_id) VALUES (?, ?)', (user_id, event_id))
                    connection.commit()
                    return "event request is pending"
    finally:
        connection.close()


def coord_event(user_id, event_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    print("Event ID:", event_id)

    cursor.execute('SELECT Coordinator_id FROM COORDINATORS WHERE user_id = ?',(user_id,))
    coordinator_id = cursor.fetchone()
    if coordinator_id:
        coordinator_id = coordinator_id[0] #this accesses the first and only element in the tuple(only one cuz we only selected one column)
    else:
        print("no co-ord found for user id")
        cursor.close()
        connection.close()
        return False
    
    
    
    cursor.execute('SELECT Coordinator_id FROM Coord_Event WHERE event_id = ? ' ,(event_id,))
    coord_from_view= cursor.fetchone()
    
    if coord_from_view:
        coord_from_view = coord_from_view[0]
        print(coord_from_view)
    else:
        print("no records for event_id", event_id)
        cursor.close()
        connection.close()
        return False

    is_coordinator = (coordinator_id == coord_from_view)
    print("is coordinator", is_coordinator)

    cursor.close()
    connection.close()
    return is_coordinator



def delete_event(event_id):
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()

    cursor.execute('DELETE FROM EVENTS WHERE Event_id = ?', (event_id,))
    connection.commit()
        
    cursor.close()
    connection.close()