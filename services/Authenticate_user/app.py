from flask import Flask, render_template, request, redirect, url_for, session, jsonify,make_response
from flask_cors import CORS
import pymysql
import mysql.connector
import requests
from uuid import uuid4
import json
import os
from dotenv import load_dotenv, dotenv_values
import sys


app = Flask(__name__, template_folder='Templates')
app.secret_key = 'your_secret_key'
CORS(app, supports_credentials=True)
user_uuid = str(uuid4())
load_dotenv()

user = os.getenv("BD_USER_NAME")
password = os.getenv("BD_PASSWORD")
bd_name = os.getenv("BD_NAME")
redirect_address = os.getenv("REDIRECT_ADDRESS")

'''
response = requests.get("http://127.0.0.1:8001/poisk", headers={'X-User-UUID': user_uuid})
'''


# Настройка подключения к базе данных
def get_db():
    try:
        connection = mysql.connector.connect(host='62.217.187.32',
                                             port='3306',
                                             database="users",
                                             user="ilfi",
                                             password="password")

        if connection.is_connected():
            db_Info = connection.get_server_info()
            print("Подключено к серверу MySQL версии", db_Info)
            cursor = connection.cursor()
            cursor.execute("SELECT DATABASE();")
            record = cursor.fetchone()
            print("Вы подключены к базе данных:", record)
            return connection

    except Exception as ex:
        print("Ошибка при подключении к MySQL")


def create_table_if_not_exists():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SHOW TABLES LIKE 'users'")
    if cursor.fetchone() is None:
        cursor.execute("""
            CREATE TABLE users (
                id INT AUTO_INCREMENT PRIMARY KEY,
                name VARCHAR(255),
                pass VARCHAR(255),
                number VARCHAR(255),
                uuid VARCHAR(255)
            )
        """)
        print("Таблица users создана")
    else:
        print("Таблица users уже существует")



'''
@app.route('/poisk')
def poisk():
    return render_template('poisk.html')
'''

'''


# Либо этот метод передачи uuid
@app.route('/poisk', methods=['GET'])
def poisk():
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT uuid FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    print(user)
    user_uuid = request.headers.get('X-User-UUID')
    if user_uuid:
        # Используйте user_uuid как вам нужно
        print(f"Получен UUID: {user_uuid}")
        # Здесь может быть ваш код для обработки UUID
        return jsonify({'message': 'UUID получен'})
    else:
        return jsonify({'error': 'UUID не предоставлен'}), 400
'''

# Либо этот метод передачи uuid
@app.route('/user/<int:user_id>/uuid')
def get_user_uuid(user_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT uuid FROM users WHERE id = %s", (user_id,))
    user = cursor.fetchone()
    print(user)
    if user:
        return jsonify({'uuid': user[0]})
    else:
        return jsonify({'error': 'User not found'}), 404


@app.route('/success')
def index():
    return render_template('index.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        number = request.form['number']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("SELECT uuid FROM users WHERE name = %s AND pass = %s AND number = %s", (username, password, number))
        user = cursor.fetchone()
        print("user: {}".format(user))
        if user:
            uuid = user
            session['uuid'] = uuid[0]
            print("test_session: {}".format(session.get("uuid")), file=sys.stderr)
            return redirect('{}:8001/friends'.format(redirect_address))
        else:
            return 'Invalid username or password'
    return render_template('login.html')


@app.route('/users/<id>', methods=['GET', 'POST'])
def ilya(id: int):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE id = {} ".format(id))
    user = cursor.fetchone()
    print(user)
    r = json.dumps(user)
    return r


def send_request(url="http://127.0.0.1:5000/poisk"):
    response = requests.get(url="{}:8001/friends".format(redirect_address))
    print(response)
    if response.status_code == 200:
        return response.json()
    else:
        return None


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        number = request.form['number']
        conn = get_db()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO users (name, pass, number, uuid) VALUES (%s, %s, %s, %s)",
                       (username, password, number, str(uuid4())))
        conn.commit()
        return redirect(url_for('login'))
    return render_template('register.html')


if __name__ == '__main__':
    create_table_if_not_exists()
    app.run(debug=True, host="0.0.0.0", port = 8080)
