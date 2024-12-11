from werkzeug.security import generate_password_hash, check_password_hash
import mysql.connector

db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'portfoliodb'
}

def connect_db():
    return mysql.connector.connect(**db_config)

conn = connect_db()
cursor = conn.cursor()

user = {
    'firstname': 'Ed Rhovic',
    'middlename': 'Banaag',
    'lastname': 'Esmas',
    'birthday': '2005-04-14',
    'age': 19,
    'contact_number': '09308472466',
    'email': 'edrhovicesmas@gmail.com',
    'username': 'edrhovic',
    'password': '041405EdRhovic'
}

hashed_password = generate_password_hash(user['password'])

check_query = """
    SELECT COUNT(*) FROM my_tb 
    WHERE username = %s OR email = %s
"""
cursor.execute(check_query, (user['username'], user['email']))
duplicate_count = cursor.fetchone()[0]

try:
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
    cursor.execute(query, values)
    conn.commit()
except mysql.connector.Error as e:
    print('')


input_password = "041405EdRhovic"
is_valid = check_password_hash(hashed_password, input_password)


cursor.close()
conn.close()
