from flask import Flask, request, jsonify, render_template, session, g, redirect, url_for, abort, flash, json
from flask_restful import Resource, Api, reqparse
from flaskext.mysql import MySQL
from flask_login import LoginManager, login_required, login_user, logout_user
from contextlib import closing
import os
import mysql.connector
from mysql.connector import Error
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename


mysql = MySQL()
app = Flask(__name__)

app.config['MYSQL_DATABASE_USER'] = 'root'
app.config['MYSQL_DATABASE_PASSWORD'] = 'jimi1310'
app.config['MYSQL_DATABASE_HOST'] = 'localhost'
app.config['MYSQL_DATABASE_DB'] = 'aso_ebi'
app.config['MYSQL_DATABASE_PORT'] = 3306
mysql.init_app(app)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = '/login'

app.config['UPLOAD_FOLDER1'] = '/home/jimi/PycharmProjects/Aso-Ebi_App/static/uploads'
app.config['UPLOAD_FOLDER2'] = '/home/jimi/PycharmProjects/Aso-Ebi_App/static/merchandise'
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg'])


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1] in ALLOWED_EXTENSIONS


@login_manager.user_loader
def load_user(user_id):
    return User.get(user_id)


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
            cursor.callproc('sp_createUser', (email, username, _hashed_password))
            data = cursor.fetchall()
            if len(data) is 0:
                conn.commit()
                return jsonify({'code': 200, 'message': 'success'})
                cursor.close()
                conn.close()
            else:
                return json.dumps({'error': str(data[0])})
        else:
            return jsonify({"Incorrect Method"})
    except Exception as e:
        return jsonify({'error', str(e)})


@app.route('/login', methods=['GET', 'POST'])
def login():
    try:
        if request.method == 'POST':
            entry = request.get_json()
            username = entry['username']
            password = entry['password']
            conn = mysql.connect()
            cursor = conn.cursor()
            query = "Select username, password, user_id from users where username = %s"
            args = username
            cursor.execute(query, args)
            data = cursor.fetchall()
            if len(data) > 0:
                if check_password_hash(str(data[0][1]), password):
                    login_user(username)
                    return jsonify('login confirmed')
                    cursor.close()
                    conn.close()
                else:
                    return jsonify('incorrect username or password')
            else:
                return jsonify('incorrect username')
        else:
            return jsonify({'error: incorrect method'})
    except Exception as e:
        print e
        return jsonify({'error', str(e)})


@app.route('/UploadProfilePhoto', methods=['GET', 'POST'])
def upload_profile_photo():
    try:
        if request.method == 'POST':
            f = request.files['file']
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER1'], filename))
                return jsonify('success')
            return 'nah'
        else:
            return jsonify('file upload failed')
    except Exception as e:
        return json.dumps({'error', str(e)})


@app.route('/getProfilePhoto', methods=['GET'])
def get_profile_photo():
    try:
        if request.method == 'GET':
            return 'we here'
        else:
            return 'you lost'
    except Exception as e:
        return jsonify({'error', str(e)})


@app.route('/search', methods=['GET'])
def search_material():
    try:
        if request.method == 'GET':
            return 'we here'
        else:
            return 'you lost'
    except Exception as e:
        return jsonify({'error', str(e)})


@app.route('/upload_material', methods=['POST'])
def upload_material():
    try:
        if request.method == 'POST':

            f = request.files['file']
            if f and allowed_file(f.filename):
                filename = secure_filename(f.filename)
                f.save(os.path.join(app.config['UPLOAD_FOLDER2'], filename))
                return jsonify('success')
            return 'nah'
        else:
            return jsonify('file upload failed')
    except Exception as e:
        return json.dumps({'error', str(e)})


if __name__ == "__main__":
    app.run()
