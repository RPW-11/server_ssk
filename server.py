from flask import Flask, render_template, request, jsonify, redirect, session
from utils import validation, db, hash
import sqlite3
from datetime import datetime, timedelta

db.set_up()
server = Flask(__name__, template_folder='templates')

ips_trials = {}
time_stamp = {}
ips_token = {}

# CONSTANTS
MAX_LOGIN_ATTEMPTS = 3
MAX_TIME_LIM = 5


@server.route("/", methods=['GET'])
def hello_world():
    return render_template('auth.html')


@server.route("/login", methods=['POST'])
def handle_login():
    validation.count_trials(ips_trials, request.remote_addr)
    data = request.form
    username = data.get('username')
    password = data.get('password')

    # hashed the py
    hashed_pw = hash.hash_password(password)
    if ips_trials[request.remote_addr] > MAX_LOGIN_ATTEMPTS:
        e = time_stamp.get(request.remote_addr)
        if e:
            cr = datetime.now() - e
            if cr > timedelta(minutes=MAX_TIME_LIM):
                del time_stamp[request.remote_addr]
                del ips_trials[request.remote_addr]
            else:
                return render_template('max_trials.html')
        else:
            time_stamp[request.remote_addr] = datetime.now()
            return render_template('max_trials.html')

    if not validation.validate_user(username, password):
        return jsonify("Invalid username or password")

    
    # query the db
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT token from users WHERE password=? AND username=?', (hashed_pw, username))
    res = cursor.fetchall()

    if len(res) == 0:
        return jsonify("Invalid username or password")
    
    del ips_trials[request.remote_addr]
    
    return redirect(f'/mydashboard/{res[0][0]}')

@server.route("/signup", methods=['POST'])
def handle_register():
    data = request.form
    username = data.get('newUsername')
    password = data.get('newPassword')
    
    if not validation.validate_user(username, password):
        redirect("/")
        return jsonify("Characters must be only alphanumeric for password and username")
    
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # check if user exists
    existing = cursor.execute("SELECT 1 from users WHERE username=?", (username,)).fetchall()
    

    if len(existing):
        return jsonify("The user already exists")

    
    # hash password
    hashed_pw = hash.hash_password(password)
    # time to store to the db
    token = hash.hash_password(username)
    cursor.execute('INSERT INTO users (username, password, token) VALUES (?, ?, ?)', (username, hashed_pw, token))
    conn.commit()

    # sec 2
    # sec 3
    conn.close()
    return redirect(f'/mydashboard/{token}')


@server.route('/mydashboard/<token>', methods=['GET'])
def render_dashboard(token):
    # validate token
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()

    # check if token is valid
    exs = cursor.execute('SELECT username from users WHERE token=?', (token,)).fetchall()

    if len(exs):
        return render_template('dashboard.html', data=exs[0])
    return render_template('page_not_found.html')


@server.route('/logout', methods=['GET'])
def logout():
    return redirect('/')




