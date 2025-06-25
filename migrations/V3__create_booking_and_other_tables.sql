CREATE TYPE booking_status_enum AS ENUM ('new', 'canceled', 'in_process', 'done');
CREATE TYPE paid_enum AS ENUM ('yes', 'no');

CREATE TABLE IF NOT EXISTS booking (
    booking_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    room_id INT NOT NULL,
    payment_id INT,
    check_in_date DATE,
    check_out_date DATE,
    guests_number INT,
    status booking_status_enum,
    price DECIMAL,
    date_creation DATE,
    paid paid_enum,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT fk_room FOREIGN KEY (room_id) REFERENCES room (room_id)
);

CREATE TABLE IF NOT EXISTS bookingstatushistory (
    booking_status_history_id SERIAL PRIMARY KEY,
    booking_id INT NOT NULL,
    old_status booking_status_enum,
    new_status booking_status_enum,
    changed_at DATE,
    CONSTRAINT fk_booking FOREIGN KEY (booking_id) REFERENCES booking (booking_id)
);

CREATE TABLE IF NOT EXISTS paymentmethod (
    payment_method_id SERIAL PRIMARY KEY,
    method_name VARCHAR(255) UNIQUE
);

CREATE TYPE payment_status_enum AS ENUM ('pending','completed','failed');

CREATE TABLE IF NOT EXISTS payment (
    payment_id SERIAL PRIMARY KEY,
    booking_id INT NOT NULL,
    payment_date DATE,
    payment_method_id INT NOT NULL,
    payment_status payment_status_enum,
    CONSTRAINT fk_booking FOREIGN KEY (booking_id) REFERENCES booking (booking_id),
    CONSTRAINT fk_payment_method FOREIGN KEY (payment_method_id) REFERENCES paymentmethod (payment_method_id)
);

CREATE TABLE IF NOT EXISTS userpaymentmethod (
    user_payment_method_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    payment_method_id INT NOT NULL,
    details VARCHAR(255),
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT fk_method FOREIGN KEY (payment_method_id) REFERENCES paymentmethod (payment_method_id)
);

CREATE TABLE IF NOT EXISTS bonus_account (
    bonus_account_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    transaction_id INT,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (user_id)
);

CREATE TABLE IF NOT EXISTS bonus_transaction (
    transaction_id SERIAL PRIMARY KEY,
    bonus_account_id INT NOT NULL,
    transaction_date DATE,
    amount DECIMAL,
    transaction_type VARCHAR(255),
    CONSTRAINT fk_bonus_acc FOREIGN KEY (bonus_account_id) REFERENCES bonus_account (bonus_account_id)
);

CREATE TABLE IF NOT EXISTS review (
    review_id SERIAL PRIMARY KEY,
    user_id INT NOT NULL,
    hotel_id INT NOT NULL,
    comment_text TEXT,
    date_creation DATE,
    CONSTRAINT fk_user FOREIGN KEY (user_id) REFERENCES users (user_id),
    CONSTRAINT fk_hotel FOREIGN KEY (hotel_id) REFERENCES hotel (hotel_id)
);

CREATE TABLE IF NOT EXISTS additional_service (
    service_id SERIAL PRIMARY KEY,
    price DECIMAL,
    service_name VARCHAR(255),
    service_description VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS booking_additional_service (
    booking_id INT NOT NULL,
    service_id INT NOT NULL,
    PRIMARY KEY (booking_id, service_id),
    CONSTRAINT fk_booking FOREIGN KEY (booking_id) REFERENCES booking (booking_id),
    CONSTRAINT fk_service FOREIGN KEY (service_id) REFERENCES additional_service (service_id)
);