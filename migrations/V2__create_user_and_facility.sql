CREATE TABLE IF NOT EXISTS users (
    user_id SERIAL PRIMARY KEY,
    bonus_account_id INT,
    name VARCHAR(255),
    second_name VARCHAR(255),
    email VARCHAR(255),
    phone VARCHAR(255),
    login VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS roomfacility (
    facility_id SERIAL PRIMARY KEY,
    facility_name VARCHAR(255) NOT NULL,
    facility_description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS room (
    room_id SERIAL PRIMARY KEY,
    hotel_id INT NOT NULL,
    capacity INT,
    price DECIMAL,
    description VARCHAR(255),
    room_type VARCHAR(255),
    CONSTRAINT fk_hotel FOREIGN KEY (hotel_id) REFERENCES hotel (hotel_id)
);

CREATE TABLE IF NOT EXISTS amenity (
    amenity_id SERIAL PRIMARY KEY,
    amenity_name VARCHAR(255),
    amenity_description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS hotelamenity (
    hotel_id INT NOT NULL,
    amenity_id INT NOT NULL,
    PRIMARY KEY (hotel_id, amenity_id),
    FOREIGN KEY (hotel_id) REFERENCES hotel (hotel_id),
    FOREIGN KEY (amenity_id) REFERENCES amenity (amenity_id)
);

CREATE TABLE IF NOT EXISTS roomhasfacility (
    room_id INT NOT NULL,
    facility_id INT NOT NULL,
    PRIMARY KEY (room_id, facility_id),
    CONSTRAINT fk_room FOREIGN KEY (room_id) REFERENCES room (room_id),
    CONSTRAINT fk_room_facility FOREIGN KEY (facility_id) REFERENCES roomfacility (facility_id)
);