ALTER TABLE instances DROP FOREIGN KEY instances_ibfk_1;
ALTER TABLE instances DROP KEY serial_number;
ALTER TABLE instances ADD CONSTRAINT fk_learner FOREIGN KEY (serial_number) REFERENCES learners (serial_number);

ALTER TABLE instances DROP FOREIGN KEY instances_ibfk_2;
ALTER TABLE instances DROP KEY bundle_id;
ALTER TABLE instances ADD CONSTRAINT fk_activity FOREIGN KEY (bundle_id) REFERENCES activities (bundle_id);


ALTER TABLE launches DROP FOREIGN KEY launches_ibfk_1;
ALTER TABLE launches DROP KEY object_id;
ALTER TABLE launches ADD CONSTRAINT fk_instance FOREIGN KEY (object_id, serial_number) REFERENCES instances (object_id, serial_number);
