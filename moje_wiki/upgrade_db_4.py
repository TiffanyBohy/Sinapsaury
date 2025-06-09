import sqlite3

conn = sqlite3.connect('wiki.db')
c = conn.cursor()

try:
    c.execute("ALTER TABLE articles ADD COLUMN grouping TEXT")
    print("Sloupec 'grouping' byl přidán.")
except sqlite3.OperationalError:
    print("Sloupec 'grouping' již existuje.")

conn.commit()
conn.close()
