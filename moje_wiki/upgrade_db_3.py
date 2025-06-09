import sqlite3

conn = sqlite3.connect('wiki.db')
c = conn.cursor()

# Přidání sloupce 'created' pokud neexistuje
try:
    c.execute("ALTER TABLE articles ADD COLUMN created TIMESTAMP DEFAULT CURRENT_TIMESTAMP")
    print("Sloupec 'created' byl přidán.")
except sqlite3.OperationalError:
    print("Sloupec 'created' již existuje.")

conn.commit()
conn.close()
