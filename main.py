from flask import Flask, jsonify
import psycopg2
from psycopg2.extras import RealDictCursor

app = Flask(__name__)

# Remote PostgreSQL connection details
app.config['POSTGRES_URL'] = 'postgresql://yourusername:yourpassword@yourhost:yourport/yourdbname'


def get_db_connection():
    connection = psycopg2.connect(app.config['POSTGRES_URL'], cursor_factory=RealDictCursor)
    return connection


@app.route('/')
def index():
    conn = get_db_connection()
    cur = conn.cursor()
    cur.execute('SELECT * FROM public.soccer_players;')
    results = cur.fetchall()
    cur.close()
    conn.close()
    print(jsonify(results))
    return jsonify(results)


if __name__ == '__main__':
    app.run(debug=True)

