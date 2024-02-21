import sqlite3
from constants import DB_PATH

def db_startup():
    conn = sqlite3.connect(DB_PATH)
    print('Database connected')
    cursor = conn.cursor()
    cursor.execute('PRAGMA foreign_keys = ON')

    ## tables
    cursor.execute('''CREATE TABLE IF NOT EXISTS CLUB_MEMBERSHIP (
        Membership_id INTEGER PRIMARY KEY AUTOINCREMENT,
        User_id INTEGER,
        Club_id INTEGER,
        Is_pending INTEGER DEFAULT 1,
        Is_approved INTEGER DEFAULT 0,
        Created DATETIME DEFAULT CURRENT_TIMESTAMP,
        Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (User_id) REFERENCES USER_DETAILS(User_id) ON DELETE CASCADE
        FOREIGN KEY (Club_id) REFERENCES CLUBS(Club_id) ON DELETE CASCADE
    );''')
    conn.commit()
    print("Club membership table created successfullly")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EVENT_ATTENDEES (
        Attendee_id INTEGER PRIMARY KEY AUTOINCREMENT,
        User_id INTEGER,
        Event_id INTEGER,
        Is_pending INTEGER DEFAULT 1,
        Is_approved INTEGER DEFAULT 0,
        Created DATETIME DEFAULT CURRENT_TIMESTAMP,
        Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (User_id) REFERENCES USER_DETAILS(User_id) ON DELETE CASCADE
        FOREIGN KEY (Event_id) REFERENCES EVENTS(Event_id) ON DELETE CASCADE
    ); ''')
    conn.commit()
    print("Event attendees table created successfullly")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS EVENTS(
      Event_id INTEGER PRIMARY KEY AUTOINCREMENT,
      EventTitle VARCHAR(20),
      Description TEXT,
      EventDate DATE,
      EventTime TIMESTAMP,
      Venue VARCHAR(50),
      Club_id INTEGER,
      Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
      Created DATETIME DEFAULT CURRENT_TIMESTAMP,
      FOREIGN Key(Club_id) REFERENCES CLUBS(Club_id) ON DELETE CASCADE
    ); ''')
    conn.commit()
    print("Events table created successfullly")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS CLUBS (
        Club_id INTEGER PRIMARY KEY AUTOINCREMENT,
        Club_name VARCHAR(40),
        Coordinator_id INTEGER,
        Description TEXT,
        Is_valid INTEGER DEFAULT 1,
        Created DATETIME DEFAULT CURRENT_TIMESTAMP,
        Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (Coordinator_id) REFERENCES COORDINATORS(Coordinator_id) ON DELETE CASCADE
    );''')
    conn.commit()
    print("Clubs table created successfullly")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS COORDINATORS (
        Coordinator_id INTEGER PRIMARY KEY AUTOINCREMENT,
        User_id INTEGER,
        Created_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        Updated_at DATETIME DEFAULT CURRENT_TIMESTAMP,
        FOREIGN KEY (User_id) REFERENCES USER_DETAILS(User_id) ON DELETE CASCADE
    );''')
    conn.commit()
    print("Coordinators table created successfullly")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS USER_LOGIN(
      Login_id INTEGER PRIMARY KEY AUTOINCREMENT,
      User_id INTEGER,
      Username VARCHAR(50) Unique,
      Password VARCHAR(70),
      Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
      Created DATETIME DEFAULT CURRENT_TIMESTAMP,
      Is_pending INT(1) DEFAULT 1,
      Is_approved INT(1) DEFAULT 0,
      CONSTRAINT UDFK FOREIGN KEY (User_id) REFERENCES USER_DETAILS (User_id) ON DELETE CASCADE
    );   ''')
    conn.commit()
    print("User login table created successfullly")

    cursor.execute('''
    CREATE TABLE IF NOT EXISTS USER_DETAILS(
      User_id INTEGER,
      Firstname VARCHAR (50),
      Lastname VARCHAR (50),
      Contact_number INTEGER,
      Email VARCHAR (80),
      Updated DATETIME DEFAULT CURRENT_TIMESTAMP,
      Created DATETIME DEFAULT CURRENT_TIMESTAMP, 
      Is_pending INT(1) DEFAULT 1,
      Is_approved INT(1) DEFAULT 0,
      CONSTRAINT UDPK PRIMARY KEY (User_id)
     );   ''')
    conn.commit()
    print("User details table created successfullly")

    ##triggers

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS updatelogin AFTER UPDATE ON USER_LOGIN
    BEGIN
        UPDATE USER_LOGIN
        SET Updated = CURRENT_TIMESTAMP
        WHERE User_id = OLD.User_id;
    END; ''')
    conn.commit()
    print("Update login trigger created successfullly")

    cursor.execute(''' 
    CREATE TRIGGER IF NOT EXISTS updateCoordinators AFTER UPDATE ON COORDINATORS 
    BEGIN
        UPDATE COORDINATORS
        SET Updated = CURRENT_TIMESTAMP
        WHERE Coordinator_id = OLD.Coordinator_id and User_id = OLD.User_id;
    END; ''')
    print("Update coordinators trigger created successfullly")

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS updatedetails AFTER UPDATE ON USER_DETAILS
    BEGIN
        UPDATE USER_DETAILS
        SET Updated = CURRENT_TIMESTAMP
        WHERE User_id = OLD.User_id;
    END; ''')
    conn.commit()
    print("Update details trigger created successfullly")

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS updateevents AFTER UPDATE ON EVENTS
    BEGIN 
        UPDATE EVENTS
        SET Updated = CURRENT_TIMESTAMP
        WHERE Event_id = OLD.Event_id;
    END; ''')
    conn.commit()
    print("Update events trigger created successfullly")

    cursor.execute('''
    
    CREATE TRIGGER IF NOT EXISTS update_clubs AFTER UPDATE ON CLUBS
    BEGIN
        UPDATE CLUBS
        SET Updated_at = CURRENT_TIMESTAMP
        WHERE Club_id = OLD.Club_id;
    END; ''')
    conn.commit()
    print("Update clubs trigger created successfullly")

    cursor.execute('''
                
    CREATE TRIGGER IF NOT EXISTS updated_trigger_club_memberships AFTER UPDATE ON CLUB_MEMBERSHIP
    BEGIN
        UPDATE CLUB_MEMBERSHIP
        SET Updated = CURRENT_TIMESTAMP
        WHERE User_id = OLD.User_id AND Club_id = OLD.Club_id;
    END; ''')
    conn.commit()
    print("Update club membership trigger created successfullly")

    cursor.execute('''
    CREATE TRIGGER IF NOT EXISTS updated_trigger_event_attendees AFTER UPDATE ON EVENT_ATTENDEES
    BEGIN
        UPDATE EVENT_ATTENDEES
        SET Updated = CURRENT_TIMESTAMP
        WHERE User_id = OLD.User_id AND Event_id = OLD.Event_id;
    END; ''')
    conn.commit()
    print("Update event attendees trigger created successfullly")

    cursor.execute('''CREATE TRIGGER IF NOT EXISTS Prevent_admin_deletion 
    BEFORE DELETE ON USER_DETAILS
    BEGIN
        SELECT CASE
            WHEN EXISTS (SELECT login_id FROM USER_LOGIN WHERE user_id = OLD.user_id AND login_id = 1) THEN
                RAISE(ABORT, 'Admin deletion not allowed')
        END;
    END ;''')
    conn.commit()
    print(" admin undeleteable trigger created")

    #views

    with sqlite3.connect(DB_PATH) as conn:
        cur = conn.cursor()

        cur.execute(''' CREATE VIEW IF NOT EXISTS USER_INFORMATION AS
            SELECT ud.user_id, ud.firstname, ud.lastname, ul.username, ud.email,contact_number
            FROM USER_DETAILS as ud
            INNER JOIN USER_LOGIN as ul
            ON ud.User_id = ul.User_id; ''')

        conn.commit()
        print("User information view created")

        cur.execute('''
            CREATE VIEW IF NOT EXISTS CLUB_AND_MEMBERS AS
            SELECT
                c.Club_name,
                u.User_id,
                u.Firstname,
                u.Lastname
            FROM CLUB_MEMBERSHIP cm
            INNER JOIN CLUBS c ON cm.Club_id = c.Club_id
            INNER JOIN USER_DETAILS u ON cm.User_id = u.User_id;
        ''')

        conn.commit()
        print("Club membership view created successfully")

    cursor.execute('''
          CREATE VIEW user_club_event AS SELECT cm.Club_id , cm.User_id ,e.Event_id, cm.Is_approved
               FROM  CLUB_MEMBERSHIP cm JOIN EVENTS e ON cm.Club_id = e.Club_id
                WHERE cm.Is_aprroved = 1;

                   ''')

    cursor.close()
    cursor.close()
    conn.close()
