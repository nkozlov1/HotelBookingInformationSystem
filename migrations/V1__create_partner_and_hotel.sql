CREATE TABLE IF NOT EXISTS partnertype (
    partner_type_id SERIAL PRIMARY KEY,
    type_name       VARCHAR(255) NOT NULL UNIQUE,
    description     VARCHAR(255)
);

CREATE TABLE IF NOT EXISTS partner (
    partner_id       SERIAL PRIMARY KEY,
    partner_type_id  INT NOT NULL,
    name             VARCHAR(255) NOT NULL,
    second_name      VARCHAR(255),
    email            VARCHAR(255),
    phone            VARCHAR(255),
    login            VARCHAR(255),
    FOREIGN KEY (partner_type_id) REFERENCES partnertype(partner_type_id)
);

CREATE TABLE IF NOT EXISTS hotel (
    hotel_id    SERIAL PRIMARY KEY,
    partner_id  INT NOT NULL,
    rating      INT,
    hotel_name  VARCHAR(255),
    address     VARCHAR(255),
    city        VARCHAR(255),
    phone  varchar(255),
    email  varchar(255),
    description VARCHAR(255),
    FOREIGN KEY (partner_id) REFERENCES partner(partner_id)
);