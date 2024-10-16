from flask import Flask, render_template
import mysql.connector
import csv
import time

app = Flask(__name__, template_folder='templates')

@app.route('/health')
def getHealth():
    return render_template("message.html", message='200')


@app.route('/')
def getData():
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

    file = open('/service3/data/data.csv', 'r')
    csv_data = csv.reader(file)

    for row in csv_data:
        cursor.execute(
            'INSERT INTO db.cities(city, population)' 'VALUES(%s, %s)',
            row)
    cnx.commit()
    print('Data is added')

    table_data = []
    for (city, pop) in cursor:
        table_data.append([city, str(pop)])

    cursor.close()
    cnx.close()

    return render_template("data.html", data=table_data)


@app.errorhandler(404)
def error404(error):
    return render_template("message.html", message='Error 404')


if __name__ == '__main__':
    app.run(host='192.170.1.4', port='5050')

