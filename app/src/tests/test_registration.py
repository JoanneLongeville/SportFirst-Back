import pytest
from unittest.mock import MagicMock
from src.connectors.authentication import handle_register_post


def test_handle_register_post_valid(mocker):
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mocker.patch('src.connectors.authentication.db_connection',
                 return_value=mock_conn)
    mock_conn.cursor.return_value = mock_cur

    # Define valid input data
    data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'role': 'user',
        'password': 'securepassword123'
    }

    response_data, response_code = handle_register_post(data)

    # Check if cursor execute method was called with the correct SQL command
    mock_cur.execute.assert_called_once_with(
        "INSERT INTO Users "
        "(firstname, lastname, email, password, phone, role) "
        "VALUES (%s, %s, %s, %s, %s, %s)",
        (data['firstname'], data['lastname'], data['email'], mocker.ANY,
         data['phone'], data['role'])
    )

    # Check if the commit method was called
    mock_conn.commit.assert_called_once()

    # Check if the cursor was closed
    mock_cur.close.assert_called_once()

    # Assert the response
    assert response_data == {'message': 'Registration successful'}
    assert response_code == 201


def test_handle_register_post_db_error(mocker):
    # Mock the database connection and cursor
    mock_conn = MagicMock()
    mock_cur = MagicMock()
    mocker.patch('src.connectors.authentication.db_connection',
                 return_value=mock_conn)
    mock_conn.cursor.return_value = mock_cur

    # Simulate a database error
    mock_cur.execute.side_effect = Exception("Database error")

    data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'john.doe@example.com',
        'phone': '1234567890',
        'role': 'user',
        'password': 'securepassword123'
    }

    response_data, response_code = handle_register_post(data)

    # Assert the response
    assert response_data == {'error': 'Registration error: Database error'}
    assert response_code == 500


def test_handle_register_post_invalid_input(mocker):
    # Invalid data with missing fields
    data = {
        'firstname': 'John',
        'lastname': 'Doe',
        'email': 'john.doe@example.com',
        # 'phone' is missing
        'role': 'user',
        'password': 'securepassword123'
    }

    with pytest.raises(KeyError):
        handle_register_post(data)
