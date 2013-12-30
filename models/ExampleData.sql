USE plugz;

INSERT INTO profile(UserName, FirstName, LastName, DateOfBirth, Gender) VALUES('xyz', 'x', 'y', '1980-2-1', 1);

INSERT INTO manufactureddevices(Identification, DeviceTypeId, DateOfManufacturing) VALUES('AABBCCDDEEF1', 1, '2013-1-1');
INSERT INTO manufactureddevices(Identification, DeviceTypeId, DateOfManufacturing) VALUES('AABBCCDDEEG2', 2, '2013-1-2');
INSERT INTO manufactureddevices(Identification, DeviceTypeId, DateOfManufacturing) VALUES('AABBCCDDEEG1', 2, '2013-1-2');
INSERT INTO manufactureddevices(Identification, DeviceTypeId, DateOfManufacturing) VALUES('BBBBCCDDEEF1', 3, '2013-1-3');
INSERT INTO manufactureddevices(Identification, DeviceTypeId, DateOfManufacturing) VALUES('BBBBCCDDEEF2', 3, '2013-1-4');
INSERT INTO manufactureddevices(Identification, DeviceTypeId, DateOfManufacturing) VALUES('CCCCCCDDEEF1', 4, '2013-1-18');
INSERT INTO manufactureddevices(Identification, DeviceTypeId, DateOfManufacturing) VALUES('CCCCCCDDEEF2', 5, '2013-1-23');
INSERT INTO manufactureddevices(Identification, DeviceTypeId, DateOfManufacturing) VALUES('CCCCCCDDEEF3', 3, '2013-1-25');
INSERT INTO manufactureddevices(Identification, DeviceTypeId, DateOfManufacturing) VALUES('CCCCCCDDEEF4', 3, '2013-1-25');

INSERT INTO device(DeviceTypeId, Identification, SubIdentification, ProfileId, HubId, Name, RegisteredDate)
            VALUES(2,            'AABBCCDDEEG2', NULL,              1,         NULL,  'Hall Hub', CURRENT_TIMESTAMP());
INSERT INTO device(DeviceTypeId, Identification, SubIdentification, ProfileId, HubId, Name, RegisteredDate)
            VALUES(3,            'BBBBCCDDEEF1', 1,                 1,         1,     'TV', CURRENT_TIMESTAMP());
INSERT INTO device(DeviceTypeId, Identification, SubIdentification, ProfileId, HubId, Name, RegisteredDate)
            VALUES(3,            'BBBBCCDDEEF1', 2,                 1,         1,     'Cable', CURRENT_TIMESTAMP());
INSERT INTO device(DeviceTypeId, Identification, SubIdentification, ProfileId, HubId, Name, RegisteredDate)
            VALUES(3,            'BBBBCCDDEEF1', 3,                 1,         1,     'Hall Light', CURRENT_TIMESTAMP());
INSERT INTO device(DeviceTypeId, Identification, SubIdentification, ProfileId, HubId, Name, RegisteredDate)
            VALUES(3,            'BBBBCCDDEEF1', 4,                 1,         1,     'Hall Fan', CURRENT_TIMESTAMP());
INSERT INTO device(DeviceTypeId, Identification, SubIdentification, ProfileId, HubId, Name, RegisteredDate)
            VALUES(4,            'CCCCCCDDEEF2', NULL,              1,         1,     'Hall Sensor', CURRENT_TIMESTAMP());

