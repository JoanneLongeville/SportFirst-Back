import psycopg2

# Database connection
def db_connection(): 
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="localhost",
                            port="5432",
                            database="sportfirst")
    return conn

def create_table():
    try:
        # Database connection
        conn = db_connection()

        # Create a cursor to execute SQL commands
        cur = conn.cursor()

        create_users_table = ''' CREATE TABLE IF NOT EXISTS Users (
            user_Id SERIAL PRIMARY KEY,
            firstname TEXT NOT NULL,
            lastname TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            phone TEXT NOT NULL,
            role TEXT
            ) '''
        
        create_roles_table = ''' CREATE TABLE IF NOT EXISTS Roles (
            role_id SERIAL PRIMARY KEY,
            role TEXT NOT NULL,
            user_Id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
            ) '''
        
        create_sessions_table = ''' CREATE TABLE IF NOT EXISTS Sessions (
            session_id SERIAL PRIMARY KEY,
            start_date_time TIMESTAMP NOT NULL,
            end_date_time TIMESTAMP NOT NULL,
            user_Id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
            ) '''
        
        create_availabilities_table = ''' CREATE TABLE IF NOT EXISTS Availabilities (
            availability_id SERIAL PRIMARY KEY,
            start_date_time TIMESTAMP NOT NULL,
            end_date_time TIMESTAMP NOT NULL,
            user_id INT NOT NULL,
            FOREIGN KEY (user_id) REFERENCES Users(user_id)
            ) '''

        # Execute SQL command
        cur.execute(create_users_table)
        cur.execute(create_roles_table)
        cur.execute(create_sessions_table)
        cur.execute(create_availabilities_table)

        # Validate changes
        conn.commit()
        print("Tables 'Users', 'Roles' 'Sessions' and 'Availabilities' created successfully")

        # Close database connection
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:   
        print("Error while creating PostgreSQL table", error)