USE plugz;

INSERT INTO country(name) VALUES('USA');
INSERT INTO states(name, country_id) VALUES('CA', 1);
INSERT INTO city(name, state_id) VALUES('Cupertino', 1);

INSERT INTO profile(username, first_name, last_name, email) VALUES('samueldotj', 'Samuel', 'Jacob', 'samueldotj@gmail.com');

INSERT INTO user_contact_info(profile_id, contact_type, address_line_1, address_line_2, city_id, postal_code, phone)
                       VALUES(1, 'Home', '10161 Beardon Dr', '4', 1, '95014', '408-744-2305');
INSERT INTO user_contact_info(profile_id, contact_type, address_line_1, address_line_2, city_id, postal_code, phone)
                       VALUES(1, 'Home', 'Another one', '4', 1, '95014', '408-744-2305');

INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, name,       appliance_type_id, registered_date)
            VALUES(2,             'AABBCCDDEEG2',  NULL,               1,          NULL,  'Hall Hub',  NULL,              CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, name,       appliance_type_id, registered_date)
            VALUES(3,             'BBBBCCDDEEF1',  1,                  1,          1,     'TV',        11,                CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, name,       appliance_type_id, registered_date)
            VALUES(3,             'BBBBCCDDEEF1',  2,                  1,          1,     'Cable',     3,                 CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, name,       appliance_type_id, registered_date)
            VALUES(3,             'BBBBCCDDEEF1',  3,                  1,          1,     'Hall Light',15,                CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, name,       appliance_type_id, registered_date)
            VALUES(3,             'BBBBCCDDEEF1',  4,                  1,          1,     'Hall Fan',  16,                CURRENT_TIMESTAMP());
INSERT INTO device(device_type_id, identification, sub_identification, profile_id, hub_id, name,       appliance_type_id, registered_date)
            VALUES(5,             'CCCCCCDDEEF2',  NULL,               1,          1,     'Hall Sensor',NULL,             CURRENT_TIMESTAMP());