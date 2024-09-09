\c sportfirst;

CREATE TABLE users
(
    id BIGSERIAL PRIMARY KEY,
    firstname VARCHAR(255),
    lastname VARCHAR(255),
    gender VARCHAR(250),
    date_of_birth DATE,
    address VARCHAR(255),
    zipcode VARCHAR(250),
    city VARCHAR(250),
    phone VARCHAR(250),
    email VARCHAR(255) UNIQUE,
    password VARCHAR(255),
    token VARCHAR(255),
    reset_token VARCHAR(255),
    role VARCHAR(50) CHECK (role IN ('admin', 'user'))

);

CREATE TABLE sessions
(
    session_id SERIAL PRIMARY KEY,
    client_id INT REFERENCES users(id),
    date_rdv DATE,
    timeslot VARCHAR(50),
    status VARCHAR(50) CHECK (status IN ('scheduled', 'completed', 'cancelled'))
);

CREATE TABLE comments
(
    comment_id SERIAL PRIMARY KEY,
    session_id INT REFERENCES sessions(session_id),
    client_id INT REFERENCES users(id),
    content TEXT,
    comment_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE availabilities
(
    availability_id SERIAL PRIMARY KEY,
    date DATE,
    timeslot VARCHAR(50),
    status VARCHAR(50) CHECK (status IN ('available', 'unavailable'))
);
