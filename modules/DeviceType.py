"""
Method to get information about a device type.
"""
from gluon import current
from modules.PlugZExceptions import *


class DeviceType:
    def __init__(self, dt):
        self.id = dt.id
        self.name = dt.Name
        self.description = dt.Description
        self.device_version = dt.DeviceVersion
        self.is_input_device = dt.IsInputDevice
        self.is_output_device = dt.IsOutputDevice
        self.image = dt.Image
        self.icon = dt.Icon

    @staticmethod
    def get_device_types():
        """
        Returns list of all device types.
        """

        db = current.db
        device_types = {}
        for dt in db().select(db.DeviceType.ALL):
            device_types[dt.id] = DeviceType(dt)
        return device_types