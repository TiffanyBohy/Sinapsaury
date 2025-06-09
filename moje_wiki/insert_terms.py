import sqlite3

conn = sqlite3.connect('wiki.db')
c = conn.cursor()

terms = [
    ("Sinapsaury", "Vyspělý biotechnologický druh", "/encyklopedie/fauna/Plazi/Sinapsaury"),
    ("NeoG", "Technologie řízení gravitace", "/encyklopedie/technologie/NeoG"),
    ("QTD", "Quantum Transposition Drive – kvantový pohon", "/Encyklopedie/Technologie/QTD")
]

c.executemany('INSERT INTO terms (name, tooltip, url) VALUES (?, ?, ?)', terms)

conn.commit()
conn.close()
print("Testovací pojmy byly vloženy.")
