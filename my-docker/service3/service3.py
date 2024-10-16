import psycopg2
import flask
import time

while True:
    try:
        con = psycopg2.connect("dbname=postgres user=debug host=postgres password=debug")
        break
    except:
        print('Connection Error')
        time.sleep(1)
cur = con.cursor()

cur.execute("""SELECT data, num FROM example""")
rows = cur.fetchall()
def create_app(rows):
    app = flask.Flask(__name__)
    app.config['rows'] = rows
    return app
app = create_app(rows)

@app.route('/', methods=['GET'])
def hey():
    table = ""
    res = dict(app.config['rows'])
    return flask.jsonify(res)

@app.route('/health', methods=['GET'])
def iwork():
    return 'http daemon working', 200

@app.errorhandler(404)
def page_not_found(e):
    return 'Page does not exist', 404

if __name__ == '__main__':
	app.run(host='httpd')