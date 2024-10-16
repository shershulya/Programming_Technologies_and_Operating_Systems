import psycopg2
import time

while True:
    try:
        con = psycopg2.connect("dbname=postgres user=debug host=postgres password=debug")
        break
    except:
        print('Connection Error')
        print('Trying Reconnect')
        time.sleep(1)

cur = con.cursor()

db_file = open('db.csv', 'r')
print('Creating table from CSV file.')
table_name = 'example'
cur.execute("""CREATE TABLE """ + table_name + """ (data varchar,num int)""")
cur.copy_from(db_file, table_name, sep= ',', columns= ('data', 'num'))
con.commit()
print('Table \'' + table_name + '\' created from CSV file.')
print('Table select first 3 rows:')
cur.execute("""SELECT data, num FROM """ + table_name)
for string in cur.fetchall()[:3]:
    print(' '.join(map(str, string)))

cur.close()
con.close()