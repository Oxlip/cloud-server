""" Module to control device objects.
"""

from gluon import current
from datetime import datetime
import PlugZExceptions
import PushNotification

from enum import Enum


class DeviceDataSource(int, Enum):
    button = 0
    current_sensor = 1
    temperature_sensor = 2
    motion_sensor = 3
    humidity_sensor = 4
    light_sensor = 5
    gas_sensor = 6


class Device(object):
    def __init__(self, device_type_id=None, identification=None, profile_id=None, hub_id=None, name=None,
                 registered_date=None, default_value=None, appliance_type_id=None):
        """
        Initializes device fields with given information.
        """
        self.id = None
        self.device_type_id = device_type_id
        self.identification = identification
        self.profile_id = profile_id
        self.hub_id = hub_id
        self.name = name
        self.registered_date = registered_date
        self.default_value = default_value
        self.appliance_type_id = appliance_type_id

    def _load(self, device):
        self.id = device.id
        self.device_type_id = device.device_type_id
        self.identification = device.identification
        self.profile_id = device.profile_id
        self.hub_id = device.hub_id
        self.name = device.name
        self.registered_date = device.registered_date
        self.default_value = device.default_value
        self.appliance_type_id = device.appliance_type_id

    @staticmethod
    def load(device_id):
        """
        Loads device information from the database into current object.
        If the device is not found then raises an exception.
        """
        db = current.db
        device = db(db.device.id == device_id).select().last()
        if device is None:
            raise PlugZExceptions.NotFoundError('Device ID not found - {id}'.format(id=device_id))

        d = Device()
        d._load(device)
        return d


    @staticmethod
    def load_by_user(user_id):
        """
        Loads device information from the database into current object.
        If the device is not found then raises an exception.
        """
        db = current.db
        device = db(db.device.profile_id == user_id).select().last()
        if device is None:
            raise PlugZExceptions.NotFoundError('Devices not found for user - {id}'.format(id=user_id))

        d = Device()
        d._load(device)
        return d



    def save(self):
        """
        Saves the current device.
        On success returns the newly created deviceId.
        """
        db = current.db
        #Check whether need to create a new record OR update existing record.
        if self.id:
            db.device(self.id).update(device_type_id=self.device_type_id,
                                      identification=self.identification,
                                      profile_id=self.profile_id,
                                      hub_id=self.hub_id,
                                      name=self.name,
                                      registered_date=self.registered_date,
                                      default_value=self.default_value,
                                      appliance_type_id=self.appliance_type_id)
        else:
            self.id = db.device.insert(device_type_id=self.device_type_id,
                                       identification=self.identification,
                                       profile_id=self.profile_id,
                                       hub_id=self.hub_id,
                                       name=self.name,
                                       registered_date=self.registered_date,
                                       default_value=self.default_value,
                                       appliance_type_id=self.appliance_type_id)

        return self.id

    def get_status_channels(self):
        """
        Returns a list of status channels on which interested parties are listening to the get updates.
        """
        #TODO - Add code to select all the channels for now it is using only owner's channel.
        from Profile import Profile
        profile = Profile.load(self.profile_id)
        if profile is None:
            raise PlugZExceptions.NotFoundError('Profile {0} not found'.format(self.profile_id))
        return [profile.get_status_channel()]

    def get_image(self, platform="web"):
        """
        Returns a best icon for this device.
        1) Based on device type the image will change.
        2) If switch then based on appliance the image change.
        3) Based platform(web, iphone, android) the image will change.
        4) If user uploaded an image it will override everything.
        """
        from DeviceType import DeviceType
        db = current.db
        if self.appliance_type_id:
            appliance_type = db(db.appliance_type.id == self.appliance_type_id).select().last()
            if appliance_type is None:
                return 'unknown.png'
            return appliance_type.image

        device_type = DeviceType.get_device_type_name(self.device_type_id)
        return '{0}.png'.format(device_type.lower())


    def record_value_change(self, timestamp, source, value, time_range):
        """
        Record a device value change(light on, current reading etc) in the database.
        """
        #Save the data in the database
        db = current.db
        db.device_data.insert(device_id=self.id, value_source=source, output_value=value, activity_date=timestamp,
                              time_range=time_range, recorded_date=datetime.now())
        db.commit()
        #push notifications to interested clients(which are connected on the device's update channel)
        PushNotification.device_update(self, source, value)

    @staticmethod
    def delete(device_id):
        """
        Deletes current device.
        On failure such as when the deviceId is not found raises an exception.
        """
        # For now we mark only the device as deleted, later we may need to modify the DeviceData and Action tables.

        db = current.db
        db(db.device.id == device_id).update(is_deleted=True)

    @staticmethod
    def get_devices_for_user(profile_id):
        """
        Returns all the devices associated with a given user.
        """
        db = current.db
        devices = []
        for d in db(db.device.profile_id == profile_id).select():
            device = Device()
            device._load(d)
            devices.append(device)
        return devices

    @staticmethod
    def get_hub_publish_channel_user(profile_id):
        """
        Returns all the devices associated with a given user.
        """
        db = current.db
        hubs = []
        for d in db(db.device.profile_id == profile_id).select(db.device.hub_id, distinct=True):
            hub = Device.load(d.hub_id)
            hubs.append(hub.identification)

        return hubs


    @staticmethod
    def get_hub_publish_channel(hub_id):
        """
        Returns channel id to publish to a hub
        """
        hub = Device.load(hub_id)
        if hub is None:
            return None
        #TODO - Security alert - For now hub identification is channel name but we should change this to a random string every time the hub connects.
        return hub.identification


    @staticmethod
    def register(serial_no, device_type_id, profile_id, device_name, hub_id=None):
        """
        Registers a device.
        This will result in creation of a new device in the device table.

        :param serial_no: Unique identification number of the device.
        :param device_type_id - Device type id - uHub, uSwitch, uPlug etc.
        :param device_name: User given name of the device.
        :param profile_id: User id.
        :param hub_id: Through which hub this device is connected.
        :return: Returns the newly created device.

        """
        db = current.db

        if hub_id:
            #check the device is already registered with the hub, just return it.
            qry = db((db.device.identification == serial_no) & (db.device.hub_id == hub_id) & (db.device.hub_id is not None))
            device = qry.select().first()
            if device:
                return device

        device = Device(device_type_id, serial_no, profile_id, hub_id, device_name, str(datetime.now()))
        device.save()
        return device
