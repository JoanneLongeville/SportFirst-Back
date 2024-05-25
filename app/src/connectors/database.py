import psycopg2
# def main():

# def create_table():
# def read_table():
# def update_table():
# def delete_table():

def create_table():
    try:
        # Connexion à la base de données
        conn = psycopg2.connect(user="postgres",
                                password="admin",
                                host="localhost",
                                port="5432",
                                database="sportfirst")
        
        # Créer un curseur pour exécuter des commandes SQL
        cur = conn.cursor()

        create_users_table = ''' CREATE TABLE IF NOT EXISTS Users (
            user_Id INT PRIMARY KEY NOT NULL,
            name TEXT NOT NULL,
            last_name TEXT NOT NULL,
            email TEXT NOT NULL,
            password TEXT NOT NULL,
            phone_number TEXT NOT NULL,
            role TEXT NOT NULL
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

        # Exécuter la commande SQL
        cur.execute(create_users_table)
        print("Table 'Users' created successfully")

        cur.execute(create_sessions_table)
        print("Table 'Sessions' created successfully")

        cur.execute(create_availabilities_table)
        print("Table 'Availabilities' created successfully")

        # Valider les modifications
        conn.commit()
        print("Tables created successfully")

        # Fermer la connexion a la base de données
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:   
        print("Error while creating PostgreSQL table", error)