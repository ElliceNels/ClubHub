import sqlite3
from constants import DB_PATH

def listOfAprrovedEvents(user_id):
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute('''SELECT EventTitle, EventDate, Is_approved FROM SUB_EVENT_DETAILS WHERE User_id = ?;''', (user_id, ))
    all_approved_events = [list(event) for event in cursor.fetchall()]
    conn.close()
    for event in all_approved_events:
        if event[2] == 1:
            event.append('Attendance approved')
        else:
            event.append('Awaiting approval')
    return all_approved_events

print(listOfAprrovedEvents(2330001))