import psycopg2

# Check if table already exists
# Create table if it does not exist
# Create columns for the table
# Close the connection to the database


# def main():

# def database_connection():

# def create_table():
# def update_table():
# def delete_table():

# def insert_data():
# def select_data():
# def update_data():
# def delete_data():


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

        # Créer une table
        sql = ''' CREATE TABLE Users (
            User_Id INT PRIMARY KEY NOT NULL,
            Name TEXT NOT NULL,
            Last_name TEXT NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            Phone_number TEXT NOT NULL,
            Role TEXT NOT NULL
            ) '''

        # Exécuter la commande SQL
        cur.execute(sql)

        # Valider les modifications
        conn.commit()
        print("Table created successfully")

        # Fermer la connexion a la base de données
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:   
        print("error while creating PostgreSQL table", error)

create_table()