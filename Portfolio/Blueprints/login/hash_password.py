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

# Hash user password
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

# Insert user data
try:
    conn = connect_db()
    cursor = conn.cursor()
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
    print("User successfully registered!")
except mysql.connector.Error as e:
    print(f"Database error occurred: {e}")
finally:
    cursor.close()
    conn.close()

# Authenticate user
try:
    conn = connect_db()
    cursor = conn.cursor()
    input_password = "041405EdRhovic"
    cursor.execute("SELECT * FROM my_tb WHERE username=%s", (user['username'],))
    usr = cursor.fetchone()
    if usr and check_password_hash(usr[9], input_password): 
        print("Login successful: User and password match.")
    else:
        print("Login failed: User and password do not match.")
except mysql.connector.Error as e:
    print(f"Database error occurred: {e}")
finally:
    cursor.close()
    conn.close()
