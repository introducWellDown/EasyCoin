import sqlite3
import time
count = 0
while True:
    # Открыть соединение с базой данных
    db = sqlite3.connect('server.db')
    cursor = db.cursor()

    # Выполнить SELECT-запрос
    cursor.execute("SELECT * FROM users")
    rows = cursor.fetchall()

    # Открыть файл для записи
    filename = 'output.txt'
    with open(filename, 'w',encoding='utf-8') as file:
        # Пройти по каждой строке результата запроса и записать ее в файл
        for row in rows:
            file.write(str(row) + '\n')

    # Закрыть файл и соединение с базой данных
    db.close()

    print(f'Значения из базы данных сохранены в файл. Цикл {count}', filename)
    count +=1
    time.sleep(30)
