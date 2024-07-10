import psycopg2
from connectors.database import db_connection
from datetime import datetime
import logging


# POST Reservation
def handle_reservation_post(data):
    start_date_time = data.get('start')
    end_date_time = data.get('end')
    user_id = data.get('userId')
    logging.warning("Reservation request: " + str(data))

    if not all([start_date_time, end_date_time, user_id]):
        return {'error': 'Missing data. Please provide start_date_time, '
                'end_date_time, and user_id.'}, 400

    if not isinstance(start_date_time, str) or not isinstance(
        end_date_time, str
    ):
        return {'error': 'Invalid data type. '
                'start_date_time and end_date_time must be strings.'}, 400

    # Verify date format
    try:
        start_date_time = datetime.fromisoformat(start_date_time)
        end_date_time = datetime.fromisoformat(end_date_time)

    except ValueError as error:
        return {'error': 'Date format error: ' + str(error)}, 400

    # Add reservation
    try:
        # Database connection
        conn = db_connection()
        cur = conn.cursor()

        # Check if there's already a reservation
        cur.execute("SELECT COUNT(*) FROM Sessions "
                    "WHERE start_date_time = %s AND end_date_time = %s",
                    (start_date_time, end_date_time))
        count = cur.fetchone()[0]

        if count > 0:
            return {'error': 'A reservation with the same start_date_time, '
                    'and end_date_time already exists.'}, 400

        # Add reservation
        cur.execute("INSERT INTO Sessions "
                    "(user_id, start_date_time, end_date_time) "
                    "VALUES (%s, %s, %s)",
                    (user_id, start_date_time, end_date_time))
        conn.commit()
        cur.close()

        response_data = {'message': 'Reservation successful'}
        response_code = 201
    except psycopg2.Error as error:
        response_data = {'error':
                         'Reservation error: ' + str(error)}
        response_code = 500
    return response_data, response_code


def main():
    print("welcome to SportFirst")


if __name__ == "__main__":
    main()
