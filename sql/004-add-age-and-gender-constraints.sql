UPDATE learners SET learners.birthdate = 0 WHERE learners.birthdate is NULL;
UPDATE learners SET learners.gender = '' WHERE learners.gender is NULL;
ALTER TABLE learners DROP PRIMARY KEY, ADD PRIMARY KEY (serial_number, birthdate, gender);


ALTER TABLE instances ADD COLUMN (birthdate INT(11) NOT NULL);
UPDATE instances, learners SET instances.birthdate = learners.birthdate WHERE instances.serial_number = learners.serial_number;

ALTER TABLE instances ADD COLUMN (gender VARCHAR(6) NOT NULL);
UPDATE instances, learners SET instances.gender = learners.gender WHERE instances.serial_number = learners.serial_number;

ALTER TABLE instances DROP PRIMARY KEY, ADD PRIMARY KEY (object_id, serial_number, birthdate, gender);
ALTER TABLE instances DROP FOREIGN KEY fk_learner;
ALTER TABLE instances ADD CONSTRAINT fk_learner FOREIGN KEY (serial_number, birthdate, gender) REFERENCES learners (serial_number, birthdate, gender);


ALTER TABLE launches ADD COLUMN (birthdate INT(11) NOT NULL);
UPDATE launches, learners SET launches.birthdate = learners.birthdate WHERE launches.serial_number=learners.serial_number;

ALTER TABLE launches ADD COLUMN (gender VARCHAR(6) NOT NULL);
UPDATE launches, learners SET launches.gender = learners.gender WHERE launches.serial_number=learners.serial_number;

ALTER TABLE launches DROP PRIMARY KEY, ADD PRIMARY KEY (timestamp, object_id, serial_number, birthdate, gender);
ALTER TABLE launches DROP FOREIGN KEY fk_instance;
ALTER TABLE launches ADD CONSTRAINT fk_instance FOREIGN KEY (object_id, serial_number, birthdate, gender) REFERENCES instances (object_id, serial_number, birthdate, gender);
