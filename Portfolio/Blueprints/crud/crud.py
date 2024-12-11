from flask import Blueprint, render_template, redirect, url_for, session, request, flash, make_response
import mysql.connector
from validation.validation import validate_user_data

crud = Blueprint('crud', __name__, template_folder='templates')

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'portfoliodb'
}

def make_header(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, proxy-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

def connect_db():
    return mysql.connector.connect(**db_config)

@crud.route('/create', methods=['POST', 'GET'])
def create():

    if 'loggedIn' in session:
        if request.method == 'POST':
            
            firstname = request.form.get('firstname').title().strip()
            middlename = request.form.get('middlename').title().strip()
            lastname = request.form.get('lastname').title().strip()
            birthday = request.form.get('birthday').strip()
            age = request.form.get('age').strip()
            contact = request.form.get('contact').strip()
            email = request.form.get('email').strip()

            errors = validate_user_data(firstname, middlename, lastname, contact, email, birthday, age)

            if errors:
                for error in errors:
                    flash(error, category='error')
                response = make_response(redirect(url_for('crud.read')))
                return make_header(response)

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crud_tb WHERE email=%s OR contact=%s", (email, contact))
            usr = cursor.fetchone()
            if usr:
                if usr[7] == email:
                    flash("Email is already registered.", category='error')
                if usr[6] == contact:
                    flash("Contact number is already registered.", category='error')
                cursor.close()
                conn.close()
                response = make_response(redirect(url_for('crud.read')))
                return make_header(response)

            cursor.execute("INSERT INTO crud_tb (firstname, middlename, lastname, birthday, age, contact, email) VALUES(%s, %s, %s, %s, %s, %s, %s)", 
                           (firstname, middlename, lastname, birthday, age, contact, email))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Account created successfully!", category='success')
            response = make_response(redirect(url_for('crud.read')))
            return make_header(response)

        response = make_response(render_template('users.html'))
        return make_header(response)

@crud.route('/read')
def read():
    if 'loggedIn' not in session:
        flash("Please log in to access this page.", category='error')
        response = make_response(redirect(url_for('auth.login')))
        return make_header(response)

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM crud_tb")
    datas = cursor.fetchall()
    cursor.close()
    conn.close()
    response = make_response(render_template('users.html', datas=datas))
    return make_header(response)

@crud.route('/update/<int:id>', methods=['POST', 'GET'])
def update(id):
    if 'loggedIn' in session:
        if request.method == 'POST':
            firstname = request.form.get('firstname').title().strip()
            middlename = request.form.get('middlename').title().strip()
            lastname = request.form.get('lastname').title().strip()
            birthday = request.form.get('birthday').strip()
            age = request.form.get('age').strip()
            contact = request.form.get('contact').strip()
            email = request.form.get('email').strip()

            # Use the validation function
            errors = validate_user_data(firstname, middlename, lastname, contact, email, birthday, age)

            if errors:
                for error in errors:
                    flash(error, category='error')
                return redirect(url_for('crud.read'))

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM crud_tb WHERE id=%s", (id,))
            usr = cursor.fetchone()

            if usr:
                cursor.execute("SELECT * FROM crud_tb WHERE (email=%s OR contact=%s) AND id!=%s", (email, contact, id))
                existing_user = cursor.fetchone()

                if existing_user:
                    if existing_user[7] == email:
                        flash("Email is already registered.", category='error')
                    if existing_user[6] == contact:
                        flash("Contact number is already registered.", category='error')
                    cursor.close()
                    conn.close()
                    return redirect(url_for('crud.read'))

                if (usr[1].strip() != firstname.strip() or usr[2].strip() != middlename.strip() or usr[3].strip() != lastname.strip() or 
                    usr[4] != birthday or usr[5] != age or usr[6].strip() != contact.strip() or usr[7].strip() != email.strip()):
                    
                    cursor.execute("UPDATE crud_tb SET firstname=%s, middlename=%s, lastname=%s, birthday=%s, age=%s, contact=%s, email=%s WHERE id=%s", 
                                (firstname, middlename, lastname, birthday, age, contact, email, id))
                    conn.commit()
                    flash("Account updated successfully", category='success')
                else:
                    flash("No changes were made", category='info') 


            cursor.close()
            conn.close()
            return redirect(url_for('crud.read'))

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM crud_tb WHERE id=%s", (id,))
        usr = cursor.fetchone()
        cursor.close()
        conn.close()

        if usr:
            return render_template('users.html', usr=usr)
        else:
            flash("User not found", category='error')
            return redirect(url_for('crud.read'))

    return redirect(url_for('auth.login'))

@crud.route('/delete/<int:id>', methods=['POST'])
def delete(id):
    if request.method == 'POST':
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("DELETE FROM crud_tb WHERE id=%s", (id,))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Account deleted successfully!", category='success')
        return redirect(url_for('crud.read'))
