CREATE TABLE counters (
    timestamp INT(11),
    download BIGINT UNSIGNED,
    upload BIGINT UNSIGNED,
    serial_number VARCHAR(255),
    birthdate INT(11),
    gender VARCHAR(6),
    grouping VARCHAR(255),
    PRIMARY KEY (timestamp, serial_number, birthdate, gender, grouping),
    KEY fk_learner_counter (serial_number, birthdate, gender, grouping),
    CONSTRAINT fk_learner_counter FOREIGN KEY (serial_number, birthdate, gender, grouping) REFERENCES learners (serial_number, birthdate, gender, grouping)
);
