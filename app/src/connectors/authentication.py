import psycopg2
import bcrypt
import getpass
from connectors.database import db_connection


# POST
def handle_register_post(data):
    firstname = data.get('firstname')
    lastname = data.get('lastname')
    email = data.get('email')
    phone = data.get('phone')
    role = data.get('role')
    password = data.get('password')

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    # Add user
    try:
        conn = db_connection()
        cur = conn.cursor()
        cur.execute("INSERT INTO Users (firstname, lastname, email, password, phone, role) VALUES (%s, %s, %s, %s, %s, %s)",
                    (firstname, lastname, email, hashed_password, phone, role))
        conn.commit()
        cur.close()

        response_data = {'message': 'Registration successful'}
        response_code = 201
    except psycopg2.Error as error:
        response_data = {'error':
                         'Registration error, please contact admin@sportfirst.com: ' + str(error)}
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

    if row and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')):
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
        choice = input("Click Register to register, Login to log in, or Logout to logout: ")
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
