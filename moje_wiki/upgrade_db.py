import sqlite3

conn = sqlite3.connect('wiki.db')
c = conn.cursor()

# Přidání sloupce 'category' pokud neexistuje
try:
    c.execute("ALTER TABLE articles ADD COLUMN category TEXT")
    print("Sloupec 'category' byl přidán.")
except sqlite3.OperationalError:
    print("Sloupec 'category' již existuje.")

conn.commit()
conn.close()