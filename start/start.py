from flask import Flask, request, jsonify, render_template, session, g, redirect, url_for, abort, flash, json
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from contextlib import closing
import os
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash

mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jimi1310'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'aso_ebi'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)


@app.route("/")
def index():
    return 'welcome to Ase-Ebi'


@app.route('/create_account', methods=['POST'])
def create_account():
    try:
        if request.method == 'POST':
            entry = request.get_json()
            email = entry['email']
            username = entry['username']
            password = entry['password']
            _hashed_password = generate_password_hash(password)
            conn = mysql.connect()
            cursor = conn.cursor()
            check = "SELECT username FROM users"
            cursor.execute(check)
            check_username = cursor.fetchall()
            for users in check_username:
                if username not in users:
                    query = "INSERT INTO users(email,username,password) VALUES(%s,%s,%s)"
                    args = (email, username, _hashed_password)
                    cursor.execute(query, args)
                    data = cursor.fetchall()
                    if data is not None:
                        conn.commit()
                        return jsonify({'code': 200, 'message': 'success'})
                        cursor.close()
                        conn.close()
                    else:
                        return json.dumps({'error': str(data[0])})
                else:
                    return jsonify({'username exists'})
        else:
            return jsonify({"Incorrect Method"})
    except Exception as e:
        return jsonify({'error', str(e)})


@app.route('/login', methods=['POST', 'GET'])
def login():
    try:
        if request.method == 'POST':
            return jsonify({'success: successful login'})
        else:
            return jsonify({'error: incorrect method'})
    except Exception as e:
        return jsonify({'error', str(e)})


if __name__ == "__main__":
    app.run()
