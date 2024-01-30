import sqlite3
conn = sqlite3.connect('Clubhub.db')
print('Database connected')
cursor = conn.cursor()

sql = """ 
-- tables

CREATE TABLE CLUB_MEMBERSHIP (
    Uid INTEGER,
    Cid INTEGER,
    Created DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (Uid, Cid)
);

CREATE TABLE EVENT_ATTENDEES (
    Uid INTEGER,
    Eid INTEGER,
    Created DATETIME DEFAULT CURRENT_TIMESTAMP,
    Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
    PRIMARY KEY (Uid, Eid)
);

CREATE TABLE IF NOT EXISTS CLUBS (
               Cid INTEGER PRIMARY KEY,
               Club_name VARCHAR(40),
               Uid INTEGER,
               Description TEXT,
               Validity_status VARCHAR(20),
               Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
               Updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
               FOREIGN KEY (Uid) REFERENCES USER_LOGIN(Uid)
        );


CREATE TABLE IF NOT EXISTS USER_TYPE (
               Uid INTEGER PRIMARY KEY,
               Type VARCHAR(20),
               Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
               Updated_at DATETIME DEFAULT CURRENT_TIMESTAMP
        );
        
--triggers

CREATE TRIGGER updated_trigger_club_memberships AFTER UPDATE ON CLUB_MEMBERSHIP
BEGIN
    UPDATE CLUB_MEMBERSHIP
    SET Updated = CURRENT_TIMESTAMP
    WHERE Uid = OLD.Uid AND Cid = OLD.Cid;
END;

CREATE TRIGGER updated_trigger_event_attendees AFTER UPDATE ON EVENT_ATTENDEES
BEGIN
    UPDATE EVENT_ATTENDEES
    SET Updated = CURRENT_TIMESTAMP
    WHERE Uid = OLD.Uid AND Eid = OLD.Eid;
END;

 CREATE TRIGGER update_clubs AFTER UPDATE ON CLUB_LIST
            BEGIN
               UPDATE CLUB_LIST
               SET Updated_at = CURRENT_TIMESTAMP
               WHERE Cid = OLD.Cid;
            END;
        );

CREATE TRIGGER update_user_type AFTER UPDATE ON USER_TYPE
            BEGIN
               UPDATE USER_TYPE
               SET Updated_at = CURRENT_TIMESTAMP
               WHERE Uid = OLD.Uid;
            END;
"""


cursor.close()
conn.close()
