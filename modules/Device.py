""" Module to control device objects.
"""

from gluon import current
from datetime import datetime
import PlugZExceptions
import PushNotification

class Device:
    def __init__(self, device_type_id=None, identification=None, profile_id=None, hub_id=None, name=None,
                 registered_date=None, default_value=None, appliance_id=None):
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
        self.appliance_id = appliance_id

    def _load(self, device):
        self.id = device.id
        self.device_type_id = device.device_type_id
        self.identification = device.identification
        self.profile_id = device.profile_id
        self.hub_id = device.hub_id
        self.name = device.name
        self.registered_date = device.registered_date
        self.default_value = device.default_value
        self.appliance_id = device.appliance_id

    @staticmethod
    def load(device_id):
        """
        Loads device information from the database into current object.
        If the device is not found then raises an exception.
        """
        db = current.db
        device = db(db.device.id == device_id).select().first()
        if device is None:
            raise PlugZExceptions.NotFoundError('Device ID not found - {id}'.format(id=device_id))

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
            db.device(self.id).update(device_type_id=self.device_type,
                                      identification=self.identification,
                                      profile_id=self.profile,
                                      hub_id=self.hub,
                                      name=self.name,
                                      registered_date=self.registered_date,
                                      default_value=self.default_value,
                                      appliance_id=self.appliance)
        else:
            self.id = db.device.insert(device_type_id=self.device_type,
                                       identification=self.identification,
                                       profile_id=self.profile,
                                       hub_id=self.hub,
                                       name=self.name,
                                       registered_date=self.registered_date,
                                       default_value=self.default_value,
                                       appliance_id=self.appliance)

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
        # TODO - Do actual implementation
        if self.id == 1:
            return 'desktop.png'
        elif self.id == 2:
            return 'laptop.png'
        elif self.id == 3:
            return 'ps3.png'
        elif self.id == 4:
            return 'washing-machine.png'
        elif self.id == 5:
            return 'tv.png'
        elif self.id == 6:
            return 'bulb.png'
        else:
            return 'x.png'

    def record_value_change(self, timestamp, value, time_range):
        """
        Record a device value change(light on, current reading etc) in the database.
        """
        #Save the data in the database
        db = current.db
        db.device_data.insert(device_id=self.id, output_value=value, activity_date=timestamp, time_range=time_range,
                              recorded_date=datetime.now())
        db.commit()
        #push notifications to interested clients(which are connected on the device's update channel)
        PushNotification.device_update(self, value)

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
    def get_hub_publish_channel(hub_id):
        """
        Returns channel id to publish to a hub
        """
        hub = Device.load(hub_id)
        if hub is None:
            return None
        #TODO - Security alert - For now hub identification is channel name but we should change this to a random string every time the hub connects.
        return hub.identification
