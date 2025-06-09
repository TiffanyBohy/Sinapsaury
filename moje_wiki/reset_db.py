import sqlite3

conn = sqlite3.connect('wiki.db')
c = conn.cursor()

# Smazání tabulky pokud existuje
c.execute('DROP TABLE IF EXISTS articles')

# Vytvoření nové čisté tabulky se sloupcem 'created'
c.execute('''
    CREATE TABLE articles (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL,
        content TEXT NOT NULL,
        category TEXT,
        subcategory TEXT,
        created TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
''')

conn.commit()
conn.close()

print("Databáze byla vyčištěna a tabulka 'articles' znovu vytvořena.")
