BEGIN TRANSACTION;
CREATE TABLE IF NOT EXISTS "CLUB_MEMBERSHIP" (
	"Membership_id"	INTEGER,
	"User_id"	INTEGER,
	"Club_id"	INTEGER,
	"Is_pending"	INTEGER DEFAULT 1,
	"Is_approved"	INTEGER DEFAULT 0,
	"Created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"Updated"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("Membership_id" AUTOINCREMENT),
	FOREIGN KEY("Club_id") REFERENCES "CLUBS"("Club_id") ON DELETE CASCADE,
	FOREIGN KEY("User_id") REFERENCES "USER_DETAILS"("User_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "EVENT_ATTENDEES" (
	"Attendee_id"	INTEGER,
	"User_id"	INTEGER,
	"Event_id"	INTEGER,
	"Is_pending"	INTEGER DEFAULT 1,
	"Is_approved"	INTEGER DEFAULT 0,
	"Created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"Updated"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("Attendee_id" AUTOINCREMENT),
	FOREIGN KEY("Event_id") REFERENCES "EVENTS"("Event_id") ON DELETE CASCADE,
	FOREIGN KEY("User_id") REFERENCES "USER_DETAILS"("User_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "EVENTS" (
	"Event_id"	INTEGER,
	"EventTitle"	VARCHAR(20) NOT NULL,
	"Description"	TEXT,
	"EventDate"	DATE NOT NULL,
	"EventTime"	TIMESTAMP NOT NULL,
	"Venue"	VARCHAR(50),
	"Club_id"	INTEGER,
	"Updated"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"Created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("Event_id" AUTOINCREMENT),
	FOREIGN KEY("Club_id") REFERENCES "CLUBS"("Club_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "CLUBS" (
	"Club_id"	INTEGER,
	"Club_name"	VARCHAR(40) UNIQUE NOT NULL,
	"Coordinator_id"	INTEGER UNIQUE,
	"Description"	TEXT,
	"Is_valid"	INTEGER DEFAULT 1,
	"Created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"Updated"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("Club_id" AUTOINCREMENT),
	FOREIGN KEY("Coordinator_id") REFERENCES "COORDINATORS"("Coordinator_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "COORDINATORS" (
	"Coordinator_id"	INTEGER,
	"User_id"	INTEGER UNIQUE NOT NULL,
	"Created_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"Updated_at"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	PRIMARY KEY("Coordinator_id" AUTOINCREMENT),
	FOREIGN KEY("User_id") REFERENCES "USER_DETAILS"("User_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "USER_LOGIN" (
	"Login_id"	INTEGER,
	"User_id"	INTEGER UNIQUE NOT NULL,
	"Username"	VARCHAR(50) UNIQUE NOT NULL,
	"Password"	VARCHAR(70) NOT NULL,
	"Updated"	DATETIME DEFAULT CURREN4T_TIMESTAMP,
	"Created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"Is_pending"	INT(1) DEFAULT 1,
	"Is_approved"	INT(1) DEFAULT 0,
	PRIMARY KEY("Login_id" AUTOINCREMENT),
	CONSTRAINT "UDFK" FOREIGN KEY("User_id") REFERENCES "USER_DETAILS"("User_id") ON DELETE CASCADE
);
CREATE TABLE IF NOT EXISTS "USER_DETAILS" (
	"User_id"	INTEGER UNIQUE NOT NULL,
	"Firstname"	VARCHAR(50) NOT NULL,
	"Lastname"	VARCHAR(50) NOT NULL,
	"Contact_number"	INTEGER,
	"Email"	VARCHAR(80) UNIQUE NOT NULL,
	"Updated"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"Created"	DATETIME DEFAULT CURRENT_TIMESTAMP,
	"Is_pending"	INT(1) DEFAULT 1,
	"Is_approved"	INT(1) DEFAULT 0,
	CONSTRAINT "UDPK" PRIMARY KEY("User_id")
);
CREATE TRIGGER updatelogin AFTER UPDATE ON USER_LOGIN
    BEGIN
        UPDATE USER_LOGIN
        SET Updated = CURRENT_TIMESTAMP
        WHERE User_id = OLD.User_id;
    END;
CREATE TRIGGER updateCoordinators AFTER UPDATE ON COORDINATORS 
    BEGIN
        UPDATE COORDINATORS
        SET Updated = CURRENT_TIMESTAMP
        WHERE Coordinator_id = OLD.Coordinator_id and User_id = OLD.User_id;
    END;
CREATE TRIGGER updatedetails AFTER UPDATE ON USER_DETAILS
    BEGIN
        UPDATE USER_DETAILS
        SET Updated = CURRENT_TIMESTAMP
        WHERE User_id = OLD.User_id;
    END;
CREATE TRIGGER updateevents AFTER UPDATE ON EVENTS
    BEGIN 
        UPDATE EVENTS
        SET Updated = CURRENT_TIMESTAMP
        WHERE Event_id = OLD.Event_id;
    END;
CREATE TRIGGER update_clubs AFTER UPDATE ON CLUBS
    BEGIN
        UPDATE CLUBS
        SET Updated_at = CURRENT_TIMESTAMP
        WHERE Club_id = OLD.Club_id;
    END;
CREATE TRIGGER updated_trigger_club_memberships AFTER UPDATE ON CLUB_MEMBERSHIP
    BEGIN
        UPDATE CLUB_MEMBERSHIP
        SET Updated = CURRENT_TIMESTAMP
        WHERE User_id = OLD.User_id AND Club_id = OLD.Club_id;
    END;
CREATE TRIGGER updated_trigger_event_attendees AFTER UPDATE ON EVENT_ATTENDEES
    BEGIN
        UPDATE EVENT_ATTENDEES
        SET Updated = CURRENT_TIMESTAMP
        WHERE User_id = OLD.User_id AND Event_id = OLD.Event_id;
    END;
CREATE TRIGGER Prevent_admin_deletion 
    BEFORE DELETE ON USER_DETAILS
    BEGIN
        SELECT CASE
            WHEN EXISTS (SELECT login_id FROM USER_LOGIN WHERE user_id = OLD.user_id AND login_id = 1) THEN
                RAISE(ABORT, 'Admin deletion not allowed')
        END;
    END;
CREATE VIEW USER_INFORMATION AS
            SELECT ud.user_id, ud.firstname, ud.lastname, ul.username, ud.email,contact_number
            FROM USER_DETAILS as ud
            INNER JOIN USER_LOGIN as ul
            ON ud.User_id = ul.User_id;
CREATE VIEW CLUB_AND_MEMBERS AS
            SELECT
                c.Club_name,
                u.User_id,
                u.Firstname,
                u.Lastname
            FROM CLUB_MEMBERSHIP cm
            INNER JOIN CLUBS c ON cm.Club_id = c.Club_id
            INNER JOIN USER_DETAILS u ON cm.User_id = u.User_id;
CREATE VIEW USER_CLUB_EVENT AS SELECT cm.Club_id , cm.User_id ,e.Event_id, cm.Is_approved
               FROM  CLUB_MEMBERSHIP cm JOIN EVENTS e ON cm.Club_id = e.Club_id
                WHERE cm.Is_approved = 1;
CREATE VIEW Coord_Event AS SELECT c.Club_id, c.Coordinator_id, e.Event_id
                FROM CLUBS c JOIN EVENTS e ON c.Club_id = e.Club_id;
CREATE VIEW SUB_EVENT_DETAILS AS 
        SELECT ea.User_id, e.EventTitle, e.EventDate, ea.Is_approved
        FROM EVENT_ATTENDEES ea INNER JOIN EVENTS e
        ON e.Event_id = ea.Event_id;
COMMIT;
