import psycopg2
import bcrypt
import getpass 


def main():
    print("Bienvenue sur SportFirst")
    while True:
        choice = input ("Cliquez sur Insciption pour vous inscrire, Connexion pour vous connecter ou Quitter pour quitter: ")
        if choice == "Inscription":
            register()
        elif choice == "Connexion":
            if login():
                while True:
                    command = input("Cliquez sur Déconnexion pour vous déconnecter").lower()
                    if command == "Déconnexion":
                        print("Déconnexion réussie")
                        break
        elif choice == "Quitter":
            break
        else:
            print("Commande invalide")
if __name__ == "__main__":
    main()


# Connexion à la base de données
def db_connection(): 
    conn = psycopg2.connect(user="postgres",
                            password="admin",
                            host="localhost",
                            port="5432",
                            database="sportfirst")
    return conn

# Ajout d'un utilisateur
def register():
    conn = db_connection()
    cur = conn.cursor()

    name = input("Entrez votre prénom: ")
    last_name = input("Entrez votre prénom: ")
    email = input("Entrez votre email: ")
    phone_number = input("Entrez votre numéro de téléphone: ")
    role = input(2)
    password = getpass.getpass("Entrez votre mot de passe: ")
    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

    try:
        cur.execute("INSERT INTO Users (name, last_name, email, password, phone_number, role) VALUES (%s, %s, %s, %s, %s, %s)", (name, last_name, email, hashed_password, phone_number, role))
        conn.commit()
        print("Inscription réussie")
    except psycopg2.IntegrityError as error:
        print("Erreur lors de l'inscription, merci de contacter admin@sportfirst.com", error)
        conn.rollback()
    finally:
        cur.close()
        conn.close()

# Connexion d'un utilisateur
def login():
    conn = db_connection()
    cur = conn.cursor()

    email = input("Entrez votre email: ")
    password = getpass.getpass("Entrez votre mot de passe: ")

    cur.execute("SELECT password FROM Users WHERE email = %s", (email,))
    row = cur.fetchone()

    cur.close()
    conn.close()

    if row and bcrypt.checkpw(password.encode('utf-8'), row[0].encode('utf-8')):
        print("Hello {name}")
        return True
    else:
        print("Email ou mot de passe incorrect")
        return False
    
# Déconnexion d'un utilisateur
def logout():
    print("Déconnexion réussie")
    return True
