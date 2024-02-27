from constants import DB_PATH
import sqlite3


class User:

    def update_user_information(self, table, column, new_value, user_id):
        conn = sqlite3.connect(DB_PATH)
        try:
            with conn:
                cursor = conn.cursor()
                update_query = f''' UPDATE {table} SET {column} = ? WHERE User_id = ?'''
                cursor.execute(update_query, (new_value, user_id))
                conn.commit()
        except sqlite3.Error as e:
            raise Exception(f"There was an error updating user information: {e}")
