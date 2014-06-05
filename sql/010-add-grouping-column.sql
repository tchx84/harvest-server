ALTER TABLE learners ADD COLUMN grouping VARCHAR(255) AFTER gender;
ALTER TABLE instances ADD COLUMN grouping VARCHAR(255) AFTER gender;
ALTER TABLE launches ADD COLUMN grouping VARCHAR(255) AFTER gender;

UPDATE learners SET learners.grouping = '';
UPDATE instances SET instances.grouping = '';
UPDATE launches SET launches.grouping = '';

SET FOREIGN_KEY_CHECKS=0;

ALTER TABLE learners DROP PRIMARY KEY, ADD PRIMARY KEY (serial_number, birthdate, gender, grouping);

ALTER TABLE instances DROP PRIMARY KEY, ADD PRIMARY KEY (object_id, serial_number, birthdate, gender, grouping);
ALTER TABLE instances DROP FOREIGN KEY fk_learner;
ALTER TABLE instances DROP KEY fk_learner;
ALTER TABLE instances ADD CONSTRAINT fk_learner FOREIGN KEY (serial_number, birthdate, gender, grouping) REFERENCES learners (serial_number, birthdate, gender, grouping);

ALTER TABLE launches DROP PRIMARY KEY, ADD PRIMARY KEY (timestamp, object_id, serial_number, birthdate, gender, grouping);
ALTER TABLE launches DROP FOREIGN KEY fk_instance;
ALTER TABLE launches DROP KEY fk_instance;
ALTER TABLE launches ADD CONSTRAINT fk_instance FOREIGN KEY (object_id, serial_number, birthdate, gender, grouping) REFERENCES instances (object_id, serial_number, birthdate, gender, grouping);

SET FOREIGN_KEY_CHECKS=1;
