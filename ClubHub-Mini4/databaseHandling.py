import sqlite3
conn = sqlite3.connect('Clubhub.db')
print('Database connected')

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
"""

cursor = conn.cursor()
