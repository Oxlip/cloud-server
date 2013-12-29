""" Module to control device objects.
"""

from gluon import current


class Device:
    def __init__(self, device_type=None, identification=None, profile=None, hub=None, name=None, registered_date=None,
                 default_value=None, appliance=None):
        """
        Initializes device fields with given information.
        @param device_type:
        @param identification:
        @param profile:
        @param hub:
        @param name:
        @param registered_date:
        @param default_value:
        @param appliance:
        """
        self.id = None
        self.device_type = device_type
        self.identification = identification
        self.profile = profile
        self.hub = hub
        self.name = name
        self.registered_date = registered_date
        self.default_value = default_value
        self.appliance = appliance

    def load(self, device_id):
        """
        Loads device information from the database into current object.
        If the device is not found then raises an exception.
        @param device_id:
        @return: @raise:
        """
        device = current.db.Device(device_id)
        if device is None:
            # TODO - define exception.
            raise

        if device.isDeleted:
            # TODO - define exception.
            raise

        self.id = device.DeviceId
        self.device_type = device.DeviceType
        self.identification = device.Identification
        self.profile = device.Profile
        self.hub = device.Hub
        self.name = device.Name
        self.registered_date = device.RegisteredDate
        self.default_value = device.DefaultValue
        self.appliance = device.Appliance

        return True

    def save(self):
        """
        Saves the current device.
        On success returns the newly created deviceId.
        @return:
        """
        db = current.db
        #Check whether need to create a new record OR update existing record.
        if self.id:
            db.Device(self.id).update(DeviceType=self.device_type,
                                      Identification=self.identification,
                                      Profile=self.profile,
                                      Hub=self.hub,
                                      Name=self.name,
                                      RegisteredDate=self.registered_date,
                                      DefaultValue=self.default_value,
                                      Appliance=self.appliance)
        else:
            self.id = db.Device.insert(DeviceType=self.device_type,
                                       Identification=self.identification,
                                       Profile=self.profile,
                                       Hub=self.hub,
                                       Name=self.name,
                                       RegisteredDate=self.registered_date,
                                       DefaultValue=self.default_value,
                                       Appliance=self.appliance)

        return self.id

    @staticmethod
    def delete(device_id):
        """
        Deletes current device.
        On failure such as when the deviceId is not found raises an exception.

        @param device_id:
        """

        # For now we mark only the device as deleted, later we may need to modify the DeviceData and Action tables.

        db = current.db
        db(db.Device.id == device_id).update(isDeleted=True)
