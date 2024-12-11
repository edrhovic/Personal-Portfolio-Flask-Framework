import re
from datetime import datetime

# Define regex patterns
name_regex = r'^[A-Za-z ]{2,}$'
contact_regex = r'^(?!.*(\d)\1{4})09\d{9}$'
birthday_regex = r'^\d{4}-\d{2}-\d{2}$'
multiple_words_regex = r'(\b\w+\b)(\s+\1){2,}'

valid_providers = [
    'gmail.com', 'yahoo.com', 'yahoo.com.ph', 'outlook.com', 'hotmail.com', 'aol.com', 
    'icloud.com', 'gov.ph', 'dfa.gov.ph', 'dip.gov.ph', 'deped.gov.ph', 'neda.gov.ph', 
    'doh.gov.ph', 'dti.gov.ph', 'dswd.gov.ph', 'dbm.gov.ph', 'pcso.gov.ph', 'pnp.gov.ph', 
    'bsp.gov.ph', 'prc.gov.ph', 'psa.gov.ph', 'dpwh.gov.ph', 'lto.gov.ph', 'boi.gov.ph',
    'hotmail.co.uk', 'hotmail.fr', 'msn.com', 'yahoo.fr', 'wanadoo.fr', 'orange.fr', 
    'comcast.net', 'yahoo.co.uk', 'yahoo.com.br', 'yahoo.com.in', 'live.com', 
    'rediffmail.com', 'free.fr', 'gmx.de', 'web.de', 'yandex.ru', 'ymail.com', 
    'libero.it', 'uol.com.br', 'bol.com.br', 'mail.ru', 'cox.net', 'hotmail.it', 
    'sbcglobal.net', 'sfr.fr', 'live.fr', 'verizon.net', 'live.co.uk', 'googlemail.com', 
    'yahoo.es', 'ig.com.br', 'live.nl', 'bigpond.com', 'terra.com.br', 'yahoo.it', 
    'neuf.fr', 'yahoo.de', 'alice.it', 'rocketmail.com', 'att.net', 'laposte.net', 
    'facebook.com', 'bellsouth.net', 'yahoo.in', 'hotmail.es', 'charter.net', 
    'yahoo.ca', 'yahoo.com.au', 'rambler.ru', 'hotmail.de', 'tiscali.it', 'shaw.ca', 
    'yahoo.co.jp', 'sky.com', 'earthlink.net', 'optonline.net', 'freenet.de', 
    't-online.de', 'aliceadsl.fr', 'virgilio.it', 'home.nl', 'qq.com', 'telenet.be', 
    'me.com', 'yahoo.com.ar', 'tiscali.co.uk', 'yahoo.com.mx', 'voila.fr', 'gmx.net', 
    'mail.com', 'planet.nl', 'tin.it', 'live.it', 'ntlworld.com', 'arcor.de', 
    'yahoo.co.id', 'frontiernet.net', 'hetnet.nl', 'live.com.au', 'yahoo.com.sg', 
    'zonnet.nl', 'club-internet.fr', 'juno.com', 'optusnet.com.au', 'blueyonder.co.uk', 
    'bluewin.ch', 'skynet.be', 'sympatico.ca', 'windstream.net', 'mac.com', 
    'centurytel.net', 'chello.nl', 'live.ca', 'aim.com', 'bigpond.net.au',
    'up.edu.ph', 'addu.edu.ph', 'ateneo.edu.ph', 'dlsu.edu.ph', 'ust.edu.ph', 'lu.edu.ph'
]

# Update email regex to restrict to valid providers
email_regex = r'^[a-zA-Z0-9._%+-]+@(' + '|'.join(valid_providers) + r')$'

def is_valid_name(name):
    return bool(re.match(name_regex, name.strip()))

def is_valid_contact(contact):
    return bool(re.match(contact_regex, contact))

def is_valid_email(email):
    email = email.strip()
    if not re.match(email_regex, email):
        return False
    local_part, domain = email.split('@')
    if len(local_part) > 64 or domain not in valid_providers:
        return False
    return True

def is_valid_birthday_and_age(birthday, age):
    if not re.match(birthday_regex, birthday):
        return False, "Invalid birthday format. Please enter a valid date (e.g., YYYY-MM-DD)."
    try:
        birthday_obj = datetime.strptime(birthday, '%Y-%m-%d')
        current_age = datetime.now().year - birthday_obj.year
        if datetime.now().month < birthday_obj.month or (datetime.now().month == birthday_obj.month and datetime.now().day < birthday_obj.day):
            current_age -= 1
        if int(age) != current_age:
            return False, "Age must be accurate based on the given birthday."

        # Validate if age is between 18 and 60
        if current_age < 18 or current_age > 60:
            return False, "Age must be between 18 and 60 years old."

        # Validate if the birthday is before or on 1964-01-01 for users aged 60 or older
        if current_age == 60 and birthday_obj > datetime(1964, 1, 1):
            return False, "Birthday must be on or before 1964-01-01 for users aged 60."

    except ValueError:
        return False, "Invalid birthday. Please ensure the date is correct."
    return True, None

def validate_user_data(firstname, middlename, lastname, contact, email, birthday, age):
    errors = []

    # Capitalize the names before validation, leave middlename empty if not provided
    firstname = firstname.strip().title()
    middlename = middlename.strip().title() if middlename else ""  # Allow empty middlename
    lastname = lastname.strip().title()

    # Validate name fields (only validate if the name is provided)
    for name, field in zip([firstname, middlename, lastname], ['First name', 'Middle name', 'Last name']):
        # Only validate if name is not empty
        if name:
            if len(name) < 2 or len(name) > 20:
                errors.append(f"{field} must be between 2 and 20 characters long.")

            elif not is_valid_name(name):
                errors.append(f"{field} must contain only letters and spaces, and be at least 2 characters long.")

            elif re.search(multiple_words_regex, name.strip()):
                errors.append(f"{field} must not have multiple words that are the same.")

            elif re.search(r'(\w)\1{3,}', name.strip()):
                errors.append(f"{field} must not have excessive character repetition.")

            elif any(len(word) < 2 for word in name.split()):
                errors.append(f"{field} must not contain words with fewer than 2 letters, unless they are common abbreviations or initials.")

            elif len(name.split()) == 1 and len(name) > 12:
                errors.append(f"{field} must consist of a single structured word.")

            elif any(len(word) > 12 for word in name.split()):
                errors.append(f"{field} must not contain a word longer than 12 characters.")

            elif '  ' in name:
                errors.append(f"{field} must not contain multiple spaces between words.")

    
    # Validate contact
    if not is_valid_contact(contact):
        if len(contact) != 11:
            errors.append("The contact number must be exactly 11 digits, with no symbols or spaces.")
        elif not contact.startswith("09"):
            errors.append("The contact number must start with 09, e.g. (09XXXXXXXXX).")
        elif re.search(r'(\d)\1{4}', contact):
            errors.append("The contact number must not contain 5 or more consecutive repeating digits.")
    
    # Validate email
    if not is_valid_email(email):
        errors.append("The email address is invalid. Please provide a valid email (e.g., Gmail, Yahoo, etc.).")

    # Validate birthday and age
    is_birthday_valid, birthday_error = is_valid_birthday_and_age(birthday, age)
    if not is_birthday_valid:
        errors.append(birthday_error)

    return errors
