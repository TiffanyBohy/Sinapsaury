import sqlite3

conn = sqlite3.connect('wiki.db')
c = conn.cursor()

# Přidání sloupce 'subcategory' pokud neexistuje
try:
    c.execute("ALTER TABLE articles ADD COLUMN subcategory TEXT")
    print("Sloupec 'subcategory' byl přidán.")
except sqlite3.OperationalError:
    print("Sloupec 'subcategory' již existuje.")

conn.commit()
conn.close()
