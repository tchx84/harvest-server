CREATE TABLE extras (
    serial_number VARCHAR(255),
    object_id CHAR(36),
    metadata_key VARCHAR(255),
    metadata_value TEXT,
    PRIMARY KEY (object_id, serial_number, metadata_key),
    FOREIGN KEY (serial_number) REFERENCES learners (serial_number)
);
