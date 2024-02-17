from constants import DB_PATH
import sqlite3


def eventsmainpage():
    connection = sqlite3.connect(DB_PATH)
    cursor = connection.cursor()
    cursor.execute('Select EventTitle, EventTime, EventDate FROM EVENTS')
    eventsmainpage = cursor.fetchall()

    cursor.close()
    connection.close()

    return eventsmainpage