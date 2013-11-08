SET FOREIGN_KEY_CHECKS=0;
UPDATE learners SET learners.serial_number = SHA1(learners.serial_number);
UPDATE instances SET instances.serial_number = SHA1(instances.serial_number);
UPDATE launches SET launches.serial_number = SHA1(launches.serial_number);
SET FOREIGN_KEY_CHECKS=1;
