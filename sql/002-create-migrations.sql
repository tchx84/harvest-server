CREATE TABLE migrations (
    filename VARCHAR(255),
    timestamp INT(11),
    PRIMARY KEY (filename)
);

INSERT INTO migrations VALUES ('001-harvest.sql', UNIX_TIMESTAMP(NOW()));
