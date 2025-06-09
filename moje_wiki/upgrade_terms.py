import sqlite3

conn = sqlite3.connect('wiki.db')
c = conn.cursor()

try:
    c.execute('''
        CREATE TABLE terms (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            name TEXT NOT NULL,
            tooltip TEXT NOT NULL,
            url TEXT NOT NULL
        )
    ''')
    print("Tabulka 'terms' byla vytvořena.")
except sqlite3.OperationalError:
    print("Tabulka 'terms' již existuje.")

conn.commit()
conn.close()
