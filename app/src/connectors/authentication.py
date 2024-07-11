import psycopg2
import bcrypt
import getpass
from .database import db_connection
import logging


# POST Register
def handle_register_post(data):
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role')
    password = data.get('password')

    try:
        # Hash password
        try:
            hashed = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
            hashed_password = hashed.decode('utf-8')
            logging.warning(type(hashed))
            logging.warning(type(hashed_password))
        except Exception as e:
            # Log hashing error
            logging.error(f"Error while hashing password: {e}")
            raise Exception("Password hashing error")

        # Add user
        conn = db_connection()
        cur = conn.cursor()
        try:
            cur.execute("INSERT INTO Users "
                        "(firstname, lastname, email, password, phone, role) "
                        "VALUES (%s, %s, %s, %s, %s, %s)",
                        (firstname, lastname, email, hashed_password, phone,
                         role))
            conn.commit()
            response_data = {'message': 'Registration successful'}
            response_code = 201

        except psycopg2.Error as error:
            conn.rollback()  # Rollback in case of database error
            response_data = {'error': 'Registration error: ' + str(error)}
            response_code = 500
        finally:
            cur.close()

    except Exception as error:
        # Handle other errors
        response_data = {'error': str(error)}
        response_code = 500

    return response_data, response_code


# POST Login
def handle_login_post(data):
    email = data.get('email')
    password = data.get('password')

    # Verify informations
    try:
        # Database connection
        conn = db_connection()
        cur = conn.cursor()

        # Execute SQL request
        cur.execute(
            """SELECT user_id, firstname, lastname, email, password, phone
            FROM Users
            WHERE email = %s
            """,
            (email,))
        resultat = cur.fetchone()

        if resultat:
            # Get user_id, firstname and hashed password from DB
            (user_id, firstname, lastname, email, hashed_password,
             phone) = resultat

            # Get hashed password from DB
            # hashed_password = resultat[0]
            logging.warning(type(password))
            logging.warning(type(hashed_password))

            # Check if password is correct
            if bcrypt.checkpw(password.encode('utf-8'),
                              hashed_password.encode('utf-8')):
                response_data = {
                                'message': 'Matching informations',
                                'userID': user_id,
                                'userFirstname': firstname,
                                'userLastname': lastname,
                                'userEmail': email,
                                'userPhone': phone
                                }
                response_code = 200
            else:
                response_data = {'message': 'Invalid email or password'}
                response_code = 401
        else:
            response_data = {'message': 'Invalid email or password'}
            response_code = 401

        conn.commit()
        cur.close()

    except psycopg2.Error as error:
        response_data = {'error':
                         'Login error: ' + str(error)}
        response_code = 500
    except ValueError as ve:
        response_data = {'error': 'ValueError: ' + str(ve)}
        response_code = 500
    except TypeError as te:
        response_data = {'error': 'TypeError: ' + str(te)}
        response_code = 500

    return response_data, response_code


def handle_profile_get(data):
    user_id = data.get('user_id')

    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("SELECT user_id, firstname, lastname, email, phone "
                    "WHERE user_id = %s", (user_id,))
        resultat = cur.fetchone()

        if resultat:
            user_id, firstname, lastname, email, phone = resultat
            response_data = {
                'userID': user_id,
                'userFirstname': firstname,
                'userLastname': lastname,
                'userEmail': email,
                'userPhone': phone
            }
            response_code = 200
        else:
            response_data = {'message': 'User not found'}
            response_code = 404

        conn.commit()
        cur.close()

    except psycopg2.Error as error:
        response_data = {'error': 'Profile retrieval error: ' + str(error)}
        response_code = 500
    except ValueError as ve:
        response_data = {'error': 'ValueError: ' + str(ve)}
        response_code = 500
    except TypeError as te:
        response_data = {'error': 'TypeError: ' + str(te)}
        response_code = 500

    return response_data, response_code


def login():
    conn = db_connection()
    cur = conn.cursor()

    email = input("Enter your e-mail: ")
    password = getpass.getpass("Enter your e-mail: ")

    cur.execute("SELECT password FROM Users WHERE email = %s", (email,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')
                              ):
        print("Hello {name}")
        return True
    else:
        print("Incorrect email or password")
        return False


# User logout
def logout():
    print("Logout successful")
    return True


def main():
    print("welcome to SportFirst")
    while True:
        choice = input("Click Register, Login, or Logout: ")
        if choice == "Register":
            handle_register_post()
        elif choice == "Login":
            if login():
                while True:
                    command = input("Click Logout to logout").lower()
                    if command == "Logout":
                        print("Logout successful")
                        break
        elif choice == "Logout":
            break
        else:
            print("Invalid command")


if __name__ == "__main__":
    main()
