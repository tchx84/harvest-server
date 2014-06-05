ALTER TABLE instances DROP COLUMN spent_time;
ALTER TABLE launches ADD COLUMN spent_time INT(11) AFTER timestamp;
