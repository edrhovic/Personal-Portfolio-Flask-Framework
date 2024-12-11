from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector


db = mysql.connector.connect(
    host="localhost",         
    user="root",              
    password="",              
    database="portfoliodb" 
)

cursor = db.cursor()

user = {
    'firstname': 'Ed Rhovic',
    'middlename': 'Banaag',
    'lastname': 'Esmas',
    'birthday': '2005-04-14',
    'age': 19,
    'contact_number': '09308472466',
    'email': 'edrhovicesmas@gmail.com',
    'username':'edrhovic',
    'password':'041405EdRhovic'
}

hashed_password = generate_password_hash(user['password'])

query = """
    INSERT INTO my_tb (firstname, middlename, lastname, birthday, age, contact, email, username, password)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
"""


values = (
    user['firstname'],
    user['middlename'],
    user['lastname'],
    user['birthday'],
    user['age'],
    user['contact_number'],
    user['email'],
    user['username'],
    hashed_password
)

cursor.close()
db.close()

