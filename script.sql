CREATE TABLE IF NOT EXISTS Users (
    id SERIAL PRIMARY KEY,
    username VARCHAR(255) NOT NULL,
    password_hash VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Auditory (
    id SERIAL PRIMARY KEY,
    number VARCHAR(255) NOT NULL,
    sector VARCHAR(255) NOT NULL
);

CREATE TABLE IF NOT EXISTS Inventory (
    id SERIAL PRIMARY KEY,
    inventory_number VARCHAR(255) NOT NULL,
    description VARCHAR(255) NOT NULL,
    commissioning_date DATE,
    auditory_id INT,
    FOREIGN KEY (auditory_id) REFERENCES Auditory(id)
);

