import sqlite3

def clearTable():
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute("DROP TABLE IF EXISTS users")  # Очистка таблицы

    db.commit()
    db.close()

clearTable()