import sqlite3
conn = sqlite3.connect('Clubhub.db')
print('Database connected')
cursor = conn.cursor()

# tables
cursor.execute('''CREATE TABLE IF NOT EXISTS CLUB_MEMBERSHIP (
    Membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    User_id INTEGER,
    Club_id INTEGER,
    Pending INTEGER DEFAULT 0,
    Status INTEGER DEFAULT 0,
    Created DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_id) REFERENCES USER_LOGIN(User_id)
    FOREIGN KEY (Club_id) REFERENCES CLUBS(Club_id)
);''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS EVENT_ATTENDEES (
    Attendee_id INTEGER PRIMARY KEY AUTOINCREMENT,
    User_id INTEGER,
    Event_id INTEGER,
    Pending INTEGER DEFAULT 0,
    Status INTEGER DEFAULT 0,
    Created DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (User_id) REFERENCES USER_LOGIN(User_id)
    FOREIGN KEY (Event_id) REFERENCES EVENTS(Event_id)
); ''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS CLUBS (
    Cid INTEGER PRIMARY KEY,
    Club_name VARCHAR(40),
    Uid INTEGER,
    Description TEXT,
    Validity_status VARCHAR(20),
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    FOREIGN KEY (Uid) REFERENCES USER_LOGIN(Uid)
);''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS USER_TYPE (
    Uid INTEGER PRIMARY KEY,
    Type VARCHAR(20),
    Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
);''')
conn.commit()

cursor.execute('''
CREATE TABLE IF NOT EXISTS USER_LOGIN(
    Uid INTEGER (8),
    Firstname VARCHAR (50),
    Lastname VARCHAR (50),
    Contactnumber INTEGER (10),
    Email VARCHAR (80),
    Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    Created DATETIME DEFAULT CURRENT_TIMESTAMP, 
    CONSTRAINT ULPK PRIMARY KEY (Uid)
); ''')
conn.commit()
 
cursor.execute('''
CREATE TABLE IF NOT EXISTS USER_DETAILS(
  Uid INTEGER (8),
  Username VARCHAR(50),
  Password VARCHAR(16),
  Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
  Created DATETIME DEFAULT CURRENT_TIMESTAMP,
  CONSTRAINT UDPK PRIMARY KEY (Uid),
  CONSTRAINT UDFK FOREIGN KEY (Uid) REFERENCES USER_LOGIN (Uid)
); ''')
conn.commit()

cursor.execute('''

CREATE TABLE IF NOT EXISTS EVENTS(
  Eid INTEGER PRIMARY KEY AUTOINCREMENT,
  EventTitle VARCHAR(20),
  Description TEXT,
  EventDate DATE,
  EventTime TIMESTAMP,
  Venue VARCHAR(50),
  Cid INTEGER,
  Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
  Created DATETIME DEFAULT CURRENT_TIMESTAMP,
  FOREIGN Key(Cid) REFERENCES CLUBS(Cid)
);''')
conn.commit()


##triggers

cursor.execute('''
CREATE TRIGGER updateevents AFTER UPDATE ON EVENTS
BEGIN 
    UPDATE EVENTS
    SET Updated = CURRENT_TIMESTAMP
    WHERE Eid = OLD.Eid;
    END;''')
conn.commit()

cursor.execute('''
CREATE TRIGGER updatelogin AFTER UPDATE ON USER_LOGIN
BEGIN
    UPDATE USER_LOGIN
    SET Updated = CURRENT_TIMESTAMP
    WHERE Uid = OLD.Uid;
END; ''')
conn.commit()

cursor.execute('''
CREATE TRIGGER updatedetails AFTER UPDATE ON USER_DETAILS
BEGIN
    UPDATE USER_DETAILS
    SET Updated = CURRENT_TIMESTAMP
    WHERE Uid = OLD.Uid;
END; ''')
conn.commit()

cursor.execute('''

CREATE TRIGGER update_clubs AFTER UPDATE ON CLUBS
BEGIN
    UPDATE CLUB_LIST
    SET Updated_at = CURRENT_TIMESTAMP
    WHERE Cid = OLD.Cid;
END; ''')
conn.commit()

cursor.execute('''
CREATE TRIGGER update_user_type AFTER UPDATE ON USER_TYPE
BEGIN
    UPDATE USER_TYPE
    SET Updated_at = CURRENT_TIMESTAMP
    WHERE Uid = OLD.Uid;
END; ''')
conn.commit()

cursor.execute('''
            
CREATE TRIGGER updated_trigger_club_memberships AFTER UPDATE ON CLUB_MEMBERSHIP
BEGIN
    UPDATE CLUB_MEMBERSHIP
    SET Updated = CURRENT_TIMESTAMP
    WHERE User_id = OLD.User_id AND Club_id = OLD.Club_id;
END; ''')
conn.commit()

cursor.execute('''
CREATE TRIGGER updated_trigger_event_attendees AFTER UPDATE ON EVENT_ATTENDEES
BEGIN
    UPDATE EVENT_ATTENDEES
    SET Updated = CURRENT_TIMESTAMP
    WHERE User_id = OLD.User_id AND Event_id = OLD.Event_id;
END; ''')
conn.commit()


cursor.close()
conn.close()

