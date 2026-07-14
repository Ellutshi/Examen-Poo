import sqlite3

conn = sqlite3.connect("edumanager.db")
conn.row_factory = sqlite3.Row
cursor = conn.cursor()

cursor.execute("SELECT * FROM etudiants")
rows = cursor.fetchall()

for row in rows:
    print("\n====================")
    for key in row.keys():
        print(f"{key} : {row[key]}")

conn.close()