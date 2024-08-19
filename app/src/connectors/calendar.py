import psycopg2
from .database import db_connection
from datetime import datetime
import logging
from flask import jsonify


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


# GET Reservations
def handle_reservations_get():
    try:
        # Database connection
        conn = db_connection()
        cur = conn.cursor()

        # Fetch reservations
        cur.execute(
            "SELECT user_id, start_date_time, end_date_time FROM Sessions")
        reservations = cur.fetchall()
        logging.warning("Reservations fetched: %s" + reservations)
        # Format the data
        reservations_data = []
        for reservation in reservations:
            user_id = reservation[0]
            start_date_time = reservation[1].isoformat()
            end_date_time = reservation[2].isoformat()

            reservations_data.append({
                'userId': user_id,
                'start': start_date_time,
                'end': end_date_time,
                'isScheduled': True
            })

        cur.close()
        # logging.warning("Fetching reservations request: %s",
        #  type(reservations_data), str(reservations_data))
        # logging.warning("Jsonify:", type(reservations_data),
        #  jsonify(str(reservations_data)))
        return jsonify(reservations_data), 200

    except psycopg2.Error as error:
        response_data = {'error': 'Error fetching reservations: ' + str(error)}
        response_code = 500

    return jsonify(response_data), response_code


# DELETE Reservation
def handle_reservation_delete(start_date_time, end_date_time, user_id):
    # logging.warning("Delete reservation request: start={}, end={}, userId={}"
    # .format(start_date_time, end_date_time, user_id))

    if not all([start_date_time, end_date_time, user_id]):
        return {'error': 'Missing data. Please provide start_date_time, '
                'end_date_time, and userId.'}, 400

    # Verify date format
    try:
        start_date_time = datetime.fromisoformat(start_date_time)
        end_date_time = datetime.fromisoformat(end_date_time)
    except ValueError as error:
        return {'error': 'Date format error: ' + str(error)}, 400

    # Delete reservation
    try:
        # Database connection
        conn = db_connection()
        cur = conn.cursor()

        # Check if the reservation exists
        cur.execute("SELECT session_id FROM Sessions "
                    "WHERE start_date_time = %s AND end_date_time = %s "
                    "AND user_id = %s",
                    (start_date_time, end_date_time, user_id))
        session_id = cur.fetchone()

        if not session_id:
            return {'error': 'No reservation found with the provided details.'
                    }, 404
        session_id = session_id[0]  # Extract session_id from the tuple

        # Delete the reservation
        cur.execute("DELETE FROM Sessions WHERE session_id = %s",
                    (session_id,))
        conn.commit()
        cur.close()

        response_data = {'message': 'Reservation successfully deleted'}
        response_code = 200
    except psycopg2.Error as error:
        response_data = {'error': 'Deletion error: ' + str(error)}
        response_code = 500

    return response_data, response_code


def main():
    print("welcome to SportFirst")


if __name__ == "__main__":
    main()
