import sqlite3
conn = sqlite3.connect('Clubhub.db')
print('Database connected')
cursor = conn.cursor()
