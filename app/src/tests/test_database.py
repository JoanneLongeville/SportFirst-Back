import pytest
import psycopg2
from src.connectors.database import db_connection, create_table


# Test database connection
def test_db_connection():
    try:
        # Call database connection function
        conn = db_connection()

        # Check if connection is psycopg2.connect object
        assert isinstance(conn, psycopg2.extensions.connection)

        # Check connection is open
        assert conn.closed == 0

        # Close connection
        conn.close()

    except Exception as e:
        pytest.fail(
            f"Erreur lors de la connexion à la base de données : {str(e)}"
            )


# Test create tables
def test_create_table():
    conn = db_connection()
    try:
        # Call function to create tables
        create_table()

        # Check tables exist in the database
        cursor = conn.cursor()

        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables"
                       " WHERE table_name = 'users')")
        assert cursor.fetchone()[0]

        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables"
                       " WHERE table_name = 'sessions')")
        assert cursor.fetchone()[0]

        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables"
                       " WHERE table_name = 'availabilities')")
        assert cursor.fetchone()[0]

        cursor.close()
    finally:
        conn.close()
