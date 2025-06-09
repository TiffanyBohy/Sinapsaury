import sqlite3

conn = sqlite3.connect('wiki.db')
c = conn.cursor()

c.execute('''
    CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL
    )
''')

conn.commit()
conn.close()
print("Databáze vytvořena.")