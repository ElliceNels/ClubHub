import sqlite3



class Inbox:


    def CoordIDtoClubID(CoordId):
        conn = sqlite3.connect('database/Clubhub.db')
        cursor = conn.cursor()









    def getUserList(self, pendingstatus, approvedstatus):
        conn = sqlite3.connect('database/Clubhub.db')
        cursor = conn.cursor()

        cursor.execute(
            ''' SELECT User_id, Firstname, Lastname FROM CLUB_MEMBERSHIP cm INNER JOIN USER_DETAILS ud ON cm.User_id = ud.User_id WHERE cm.Is_pending = ? AND User_id != ?''',(pendingstatus, approvedstatus, 4121234))
        self.userList = [list(row) for row in cursor.fetchall()]

        cursor.close()
        conn.close()
        print(self.userList)
        return self.userList

