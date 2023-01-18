import sqlite3

database = sqlite3.connect('translator.db')
cursor = database.cursor()


cursor.execute('''
CREATE TABLE IF NOT EXISTS history(
    history_id INTEGER PRIMARY KEY AUTOINCREMENT,
    telegram_id INTEGER,
    from_lang VARCHAR(50),
    to_lang VARCHAR(50),
    original_text TEXT,
    translated_text TEXT
)
''')

database.commit()
database.close()