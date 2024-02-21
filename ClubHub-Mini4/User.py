from constants import DB_PATH
import sqlite3
class User:
    
    def update_user_information(self, table, column, new_value, user_id):
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()
        
        try:
            with conn:
                update_query = f''' UPDATE {table} SET {column} = ? WHERE User_id = ?'''
                cursor.execute(update_query, ( new_value, user_id) )
                conn.commit()
        except Exception as e:
            print(e)
        finally:
            cursor.close()
            conn.close()
        