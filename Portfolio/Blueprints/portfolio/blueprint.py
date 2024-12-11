from flask import Blueprint, render_template, redirect, url_for, session, request, make_response, flash
import mysql.connector
from werkzeug.security import check_password_hash
from validation.validation import validate_user_data



blueprint = Blueprint('blueprint', __name__, template_folder='templates')

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


@blueprint.route('/')
@blueprint.route('/home')
def dashboard():
    if 'loggedIn' in session:
        first_name = session.get('firstname')
        response = make_response(render_template('dashboard.html', first_name=first_name))
        return make_header(response)

    flash("You must log in to access this page.", category='error')
    response = make_header(redirect(url_for('auth.login')))
    return make_response(response)

@blueprint.route('/blog')
def blog():
    if 'loggedIn' in session:
        response = make_response(render_template('blog.html'))
        return make_header(response)
    
    
    flash("You must login to access this page", category='error')
    response = make_response(redirect(url_for('auth.login')))
    return make_header(response)


@blueprint.route('/profile', methods=['GET', 'POST'])
def update_profile():

    if 'loggedIn' in session:
        username = session['loggedIn']

        if request.method == 'POST':
            firstname = request.form.get('firstname').title().strip()
            middlename = request.form.get('middlename').title().strip()
            lastname = request.form.get('lastname').title().strip()
            birthday = request.form.get('birthday').strip()
            age = request.form.get('age').strip()
            contact = request.form.get('contact').strip()
            email = request.form.get('email').strip().lower()

            errors = validate_user_data(firstname, middlename, lastname, contact, email, birthday, age)

            if errors:
                for error in errors:
                    flash(error, category='error')
                response = make_response(redirect(url_for('blueprint.update_profile')))
                return make_header(response)

            conn = connect_db()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM my_tb WHERE (email=%s OR contact=%s) AND username!=%s", (email, contact, username))
            existing_user = cursor.fetchone()

            if existing_user:
                if existing_user[6] == contact:
                    flash("Contact number is already registered.", category='error')
                if existing_user[7] == email:
                    flash("Email is already registered.", category='error')
                cursor.close()
                conn.close()
                return redirect(url_for('blueprint.update_profile'))
                
            cursor.execute("""
                UPDATE my_tb 
                SET firstname=%s, middlename=%s, lastname=%s, birthday=%s, age=%s, contact=%s, email=%s 
                WHERE username=%s
            """, (firstname, middlename, lastname, birthday, age, contact, email, username))
            conn.commit()
            cursor.close()
            conn.close()
            flash("Profile updated successfully!", category='success')
            response = make_response(redirect(url_for('blueprint.update_profile')))
            return make_header(response)
            
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM my_tb WHERE username=%s", (username,))
        user_data = cursor.fetchone()
        cursor.close()
        conn.close()

        if user_data:
            response = make_response(render_template('profile.html', usr=user_data))
            return make_header(response)

        flash("User not found.", category='error')  
        return redirect(url_for('blueprint.update_profile'))

    flash("You must log in to access this page.", category='error')
    response = make_response(redirect(url_for('auth.login')))
    return make_header(response)




@blueprint.route('/delete_profile', methods=['POST', 'GET'])
def delete_profile():

    if 'loggedIn' in session:
        username = session['loggedIn']
        password = request.form.get('password')

        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM my_tb WHERE username=%s", (username,))
        usr = cursor.fetchone()

        if usr and check_password_hash(usr[9], password):

            cursor.execute("DELETE FROM my_tb WHERE username=%s", (username,))
            conn.commit()
            session.clear()
            flash('Your profile has been deleted successfully!', 'success')
            response = make_response(redirect(url_for('auth.login')))
            return make_header(response)
        
        else:
            flash('Incorrect password. Please try again.', category='error')
            response = make_response(redirect(url_for('blueprint.update_profile')))
            return make_header(response)
        
    response = make_response(redirect(url_for('auth.login')))
    return make_header(response)

