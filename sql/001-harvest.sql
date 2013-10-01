
CREATE DATABASE harvest;

USE harvest;

CREATE TABLE learners (
    serial_number VARCHAR(11),
    birthdate INT(11),
    gender VARCHAR(8),
    PRIMARY KEY (serial_number)
);

CREATE TABLE activities (
    bundle_id VARCHAR(32),
    PRIMARY KEY (bundle_id)
);

CREATE TABLE instances (
    object_id VARCHAR(37),
    filesize BIGINT UNSIGNED,
    creation_time int(11),
    timestamp int(11),
    buddies int(3),
    spent_time int(11),
    share_scope BOOLEAN,
    title_set_by_user BOOLEAN,
    keep BOOLEAN,
    serial_number VARCHAR(11),
    bundle_id VARCHAR(32),
    PRIMARY KEY (object_id),
    FOREIGN KEY (serial_number) REFERENCES learners (serial_number),
    FOREIGN KEY (bundle_id) REFERENCES activities (bundle_id)
);

CREATE TABLE launches (
    timestamp INT(11) NOT NULL,
    object_id VARCHAR(37),
    PRIMARY KEY (timestamp, object_id),
    FOREIGN KEY (object_id) REFERENCES instances (object_id)
);
