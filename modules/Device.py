""" Module to control device objects.
"""

from gluon import current
from modules.PlugZExceptions import *


class Device:
    def __init__(self, device_type_id=None, identification=None, profile_id=None, hub_id=None, name=None, registered_date=None,
                 default_value=None, appliance_id=None):
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
        self.device_type_id = device_type_id
        self.identification = identification
        self.profile_id = profile_id
        self.hub_id = hub_id
        self.name = name
        self.registered_date = registered_date
        self.default_value = default_value
        self.appliance_id = appliance_id

    def _load(self, device):
        self.id = device.id
        self.device_type_id = device.DeviceTypeId
        self.identification = device.Identification
        self.profile_id = device.ProfileId
        self.hub_id = device.HubId
        self.name = device.Name
        self.registered_date = device.RegisteredDate
        self.default_value = device.DefaultValue
        self.appliance_id = device.ApplianceID

    def load(self, device_id):
        """
        Loads device information from the database into current object.
        If the device is not found then raises an exception.
        @param device_id:
        @return: @raise:
        """
        db = current.db
        device = db(db.Device.id == device_id).select()
        if device is None:
            raise NotFoundError('Device not found - {id}'.format(id=device_id))

        if device.isDeleted:
            raise MarkedAsDeleted('Device is already deleted - {id}'.format(id=device_id))

        self._load(device)

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

    @staticmethod
    def get_devices_for_user(profile_id):
        """
        Returns all the devices associated with a given user.
        """
        db = current.db
        devices = []
        for d in db(db.Device.ProfileId == profile_id).select():
            device = Device()
            device._load(d)
            devices.append(device)
        return devices