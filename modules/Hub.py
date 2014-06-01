""" Hub related functions and classes.
"""

from gluon import current
import datetime
import PlugZExceptions
from Device import Device
from DeviceType import DeviceType


class Hub(Device):
    def __init__(self, identification=None, profile_id=None, name=None, registered_date=None):
        """
        Initializes device fields with given information.
        """
        self.id = None
        self.device_type_id = DeviceType.HUB
        self.identification = identification
        self.profile_id = profile_id
        self.name = name
        self.registered_date = registered_date
        self.hub_id = None
        self.default_value = None
        self.appliance_id = None

    def _load(self, hub):
        self.id = hub.id
        self.device_type_id = hub.device_type_id
        self.identification = hub.identification
        self.profile_id = hub.profile_id
        self.name = hub.name
        self.registered_date = hub.registered_date

    @staticmethod
    def load(hub_id):
        """
        Loads hub information from the database into current object.
        If the device is not found then raises an exception.
        """
        db = current.db
        hub = db((db.device.id == hub_id) & (db.device.device_type_id == DeviceType.HUB)).select().first()
        if hub is None:
            raise PlugZExceptions.NotFoundError('Hub not found - {id}'.format(id=hub_id))

        h = Hub()
        h._load(hub)
        return h

    @staticmethod
    def load_by_identification(identification):
        """
        Loads device information from the database into current object.
        If the device is not found then raises an exception.
        """
        db = current.db
        hub = db(db.device.identification == identification).select().first()
        if hub is None:
            raise PlugZExceptions.NotFoundError('Hub not found - {id}'.format(id=identification))

        return Hub.load(hub.id)

    @staticmethod
    def get_devices(hub_id):
        """
        Returns all the devices associated with a given hub.
        """
        db = current.db
        devices = []
        for d in db(db.device.hub_id == hub_id).select():
            device = Device()
            device._load(d)
            devices.append(device)
        return devices

    @staticmethod
    def connect(hub_identification, authentication_key):
        """
        Adds a new entry in the hub_session table.
        """

        db = current.db
        # TODO - Add authentication and then generate channel name, for now the channel name is hub identification
        hub = Hub.load_by_identification(hub_identification)
        channel = hub.identification

        #disconnect any previous connections
        Hub.disconnect(hub.id)

        # Add a new entry in the hub_session table
        db.hub_session.insert(device_id=hub.id, connect_time=datetime.datetime.utcnow(), channel=channel)
        return hub.id, channel

    @staticmethod
    def disconnect(hub_id):
        """
        Disconnects a hub session
        """
        db = current.db
        sessions = db((db.hub_session.device_id == hub_id) & (db.hub_session.disconnect_time == None)).select()
        for session in sessions:
            session.disconnect_time = datetime.datetime.utcnow()
            session.update_record()

    @staticmethod
    def get_channel(hub_id):
        """
        Returns channel id to communicate with the hub(for push commands).
        """
        db = current.db
        hub_session = db((db.hub_session.device_id == hub_id) & (db.hub_session.disconnect_time == None)).select().first()
        if hub_session is None:
            #TODO - this exception is only for testing - this should be converted to log message and return ''
            raise PlugZExceptions.NotConnectedError('Hub {0} not connected'.format(hub_id))

        return hub_session.channel

    @staticmethod
    def get_channel_by_profile(profile_id):
        """
        Returns channel id to communicate with the hub(for push commands).
        """
        from Device import Device
        hubs = Device.get_devices_for_user(profile_id)
        db = current.db

        hub_sessions = []

        for hub in hubs:
            hub_session = db((db.hub_session.device_id == hub.device_id) & (db.hub_session.disconnect_time == None)).select().first()
            hub_sessions.append(hub_session.channel)

        return hub_sessions