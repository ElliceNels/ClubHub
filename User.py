import sqlite3
class User:
    
    def updateUserInformation(self, table, column, newvalue, user_id):
        conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')
        cursor = conn.cursor()
        
        try:
            with conn:
                updateQuery = f''' UPDATE {table} SET {column} = ? WHERE User_id = ?'''
                cursor.execute(updateQuery, ( newvalue, user_id) )
                conn.commit()
        except Exception as e:
            print(e)
        