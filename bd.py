import sqlite3

def createBD():
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute("""CREATE TABLE IF NOT EXISTS users (
                        id INTEGER PRIMARY KEY,
                        Eth REAL,
                        Bitcoin REAL,
                        Notification INTEGER,
                        Name TEXT
                    )""")
    db.close()

def isExistsID(userId,name):
    
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    
    cursor.execute(f'SELECT id FROM users WHERE id = {userId}')
    row = cursor.fetchone()

    if row is not None:
        pass
    else:
        cursor.execute(f'INSERT INTO users (id, Eth, Bitcoin, Notification, Name) VALUES ({userId},0,0,0,"{name}")')
        
    db.commit()
    db.close()

def outputValues(userId):
    
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    
    cursor.execute(f'SELECT * FROM users WHERE id = {userId}')
    
    
    rows = cursor.fetchall()
    
    db.close()
    
    
    columns = [column[0] for column in cursor.description]
    outputResult = []
    for row in rows:
        for i in range(1,len(columns)-2):
            outputResult.append(f"{columns[i]}: {row[i]}")
    
    
    outputResult = str(outputResult)
    
    outputResult = outputResult.replace("[", "")
    outputResult = outputResult.replace("]", "")
    outputResult = outputResult.replace(" ", "")
    outputResult = outputResult.replace("'", "")
    outputResult = outputResult.replace(":", ": ")
    outputResult = outputResult.replace(",", "\n")
    return outputResult

def updateValue(userId, columnName, newValue):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    cursor.execute(f"UPDATE users SET {columnName} = {newValue} WHERE id = {userId}")
    db.commit()

    db.close()

def changeNotificationStatus(userId):
    
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    
    cursor.execute(f'SELECT Notification FROM users WHERE id = {userId}')
    row = cursor.fetchone()
    if row[0] == 1:
        cursor.execute(f"UPDATE users SET Notification = 0 WHERE id = {userId}")
        db.commit()
        db.close()
        return False
    elif row[0] == 0:
        cursor.execute(f"UPDATE users SET Notification = 1 WHERE id = {userId}")
        db.commit()
        db.close()
        return True

def chekNotificationStatus(userId):
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    
    cursor.execute(f'SELECT Notification FROM users WHERE id = {userId}')
    row = cursor.fetchone()
    db.close()
    if row[0] == 1:
        return True
    else:
        return False

        
def outputSingleValues(userId,coin):
    
    db = sqlite3.connect('server.db')
    cursor = db.cursor()
    
    cursor.execute(f'SELECT Eth,Bitcoin FROM users WHERE id = {userId}')
    
    
    rows = cursor.fetchall()
    db.close()
    
    ethValue = rows[0][0]
    btcValue = rows[0][1]
    
    if coin == "Eth":
        return ethValue
    elif coin == "Bitcoin":
        return btcValue
    else:
        return None

