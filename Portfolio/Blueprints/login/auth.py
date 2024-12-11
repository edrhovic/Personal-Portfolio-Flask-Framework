from flask import Flask, Blueprint, render_template, redirect, url_for, make_response, session, request, flash
import mysql.connector
from werkzeug.security import check_password_hash

auth = Blueprint('auth', __name__, template_folder='templates')

db_config = {
    'host':'localhost',
    'user':'root',
    'password':'',
    'database':'portfoliodb'
}

def make_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def connect_db():
    return mysql.connector.connect(**db_config)

@auth.route('/login', methods=['POST', 'GET'])
def login():
    errorMessage = ''

    if 'loggedIn' in session:
        return redirect(url_for('blueprint.dashboard'))
    
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM my_tb WHERE username=%s", (username,))
        usr = cursor.fetchone()

        if usr and check_password_hash(usr[9], password):
            session.permanent = True
            session['loggedIn'] = username
            session['firstname'] = usr[1]
            return redirect(url_for('blueprint.dashboard'))
        else:
            errorMessage = 'Incorrect username or password'

        cursor.close()
        conn.close()

    response = make_response(render_template('login.html', errorMessage=errorMessage))
    return make_header(response)


@auth.route('/logout')
def logout():
    session.clear()
    response = make_response(redirect(url_for('auth.login')))
    return make_header(response)

