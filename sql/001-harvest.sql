
CREATE DATABASE harvest;

USE harvest;

CREATE TABLE learners (
    serial_number VARCHAR(255),
    birthdate INT(11),
    gender VARCHAR(6),
    PRIMARY KEY (serial_number)
);

CREATE TABLE activities (
    bundle_id VARCHAR(255),
    PRIMARY KEY (bundle_id)
);

CREATE TABLE instances (
    object_id CHAR(36),
    filesize BIGINT UNSIGNED,
    creation_time INT(11),
    timestamp INT(11),
    buddies TINYINT UNSIGNED,
    spent_time INT(11),
    share_scope BOOLEAN,
    title_set_by_user BOOLEAN,
    keep BOOLEAN,
    serial_number VARCHAR(255),
    bundle_id VARCHAR(255),
    PRIMARY KEY (object_id, serial_number),
    FOREIGN KEY (serial_number) REFERENCES learners (serial_number),
    FOREIGN KEY (bundle_id) REFERENCES activities (bundle_id)
);

CREATE TABLE launches (
    timestamp INT(11) NOT NULL,
    object_id CHAR(36),
    serial_number VARCHAR(255),
    PRIMARY KEY (timestamp, object_id, serial_number),
    FOREIGN KEY (object_id, serial_number) REFERENCES instances (object_id, serial_number)
);

CREATE USER 'harvest'@'localhost' IDENTIFIED BY 'harvest';
GRANT ALL PRIVILEGES ON harvest . * TO 'harvest'@'localhost';
