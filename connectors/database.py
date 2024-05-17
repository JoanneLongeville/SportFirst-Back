import psycopg2


def create_table():
    try:
        conn = psycopg2.connect(user="postgres",
                                password="admin",
                                host="localhost",
                                port="5432",
                                database="sportfirst")
        cur = conn.cursor()

        sql = ''' CREATE TABLE Users (
            User_Id INT PRIMARY KEY NOT NULL,
            Name TEXT NOT NULL,
            Last_name TEXT NOT NULL,
            Email TEXT NOT NULL,
            Password TEXT NOT NULL,
            Phone_number TEXT NOT NULL,
            Role TEXT NOT NULL
            ) '''

        cur.execute(sql)
        conn.commit()
        print("Table created successfully")

        #fermeture de la connexion a la base de données
        cur.close()
        conn.close()
        print("PostgreSQL connection is closed")

    except (Exception, psycopg2.DatabaseError) as error:   
        print("error while creating PostgreSQL table", error)

create_table()