USE plugz;

INSERT INTO country(name) VALUES('USA');
INSERT INTO states(name, country_id) VALUES('CA', 1);
INSERT INTO city(name, state_id) VALUES('Cupertino', 1);

INSERT INTO profile(username, first_name, last_name, date_of_birth, gender, email) VALUES('samueldotj', 'Samuel', 'Jacob', '1980-2-1', 1, 'samueldotj@gmail.com');

INSERT INTO user_contact_info(profile_id, contact_type, address_line_1, address_line_2, city_id, postal_code, phone)
                       VALUES(1, 'Home', '10161 Beardon Dr', '4', 1, '95014', '408-744-2305');
INSERT INTO user_contact_info(profile_id, contact_type, address_line_1, address_line_2, city_id, postal_code, phone)
                       VALUES(1, 'Home', 'Another one', '4', 1, '95014', '408-744-2305');

INSERT INTO manufactured_devices(identification, device_type_id, date_of_manufacture) VALUES('AABBCCDDEEF1', 1, '2013-1-1');
INSERT INTO manufactured_devices(identification, device_type_id, date_of_manufacture) VALUES('AABBCCDDEEG2', 2, '2013-1-2');
INSERT INTO manufactured_devices(identification, device_type_id, date_of_manufacture) VALUES('AABBCCDDEEG1', 2, '2013-1-2');
INSERT INTO manufactured_devices(identification, device_type_id, date_of_manufacture) VALUES('BBBBCCDDEEF1', 3, '2013-1-3');
INSERT INTO manufactured_devices(identification, device_type_id, date_of_manufacture) VALUES('BBBBCCDDEEF2', 3, '2013-1-4');
INSERT INTO manufactured_devices(identification, device_type_id, date_of_manufacture) VALUES('CCCCCCDDEEF1', 4, '2013-1-18');
INSERT INTO manufactured_devices(identification, device_type_id, date_of_manufacture) VALUES('CCCCCCDDEEF2', 5, '2013-1-23');
INSERT INTO manufactured_devices(identification, device_type_id, date_of_manufacture) VALUES('CCCCCCDDEEF3', 3, '2013-1-25');
INSERT INTO manufactured_devices(identification, device_type_id, date_of_manufacture) VALUES('CCCCCCDDEEF4', 3, '2013-1-25');


INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, Name, registered_date)
            VALUES(2,            'AABBCCDDEEG2', NULL,              1,         NULL,  'Hall Hub', CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, Name, registered_date)
            VALUES(3,            'BBBBCCDDEEF1', 1,                 1,         1,     'TV', CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, Name, registered_date)
            VALUES(3,            'BBBBCCDDEEF1', 2,                 1,         1,     'Cable', CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, Name, registered_date)
            VALUES(3,            'BBBBCCDDEEF1', 3,                 1,         1,     'Hall Light', CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, Name, registered_date)
            VALUES(3,            'BBBBCCDDEEF1', 4,                 1,         1,     'Hall Fan', CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, Name, registered_date)
            VALUES(5,            'CCCCCCDDEEF2', NULL,              1,         1,     'Hall Sensor', CURRENT_TIMESTAMP());