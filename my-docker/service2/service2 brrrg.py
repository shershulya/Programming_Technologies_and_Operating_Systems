import mysql.connector
import csv
import time

if __name__ == '__main__':
    print("Start connecting to database")
    is_connected = False
    while not is_connected:
        try:
            cnx = mysql.connector.connect(user='root',
                                          password='pass123',
                                          host='192.169.7.2', )
            is_connected = True
        except:
            time.sleep(1)
            print('Reconnecting...')
    print('Connected.')

    cursor = cnx.cursor()
    try:
        cursor.execute('DROP DATABASE db')
    except:
        pass
    cursor.execute('CREATE DATABASE db')
    cursor.execute('CREATE TABLE db.cities (city VARCHAR(255), population INTEGER)')
    print('Database is created')

    file = open('/service2/data/data.csv', 'r')
    csv_data = csv.reader(file)

    for row in csv_data:
        cursor.execute(
            'INSERT INTO db.cities(city, population)' 'VALUES(%s, %s)',
            row)
    cnx.commit()
    print('Data is added')

    cursor.execute('SELECT * FROM db.cities')
    cnt = 0
    for (city, pop) in cursor:
        cnt += 1
        print("{}:\t{}".format(city, pop))

    cursor.close()
    cnx.close()