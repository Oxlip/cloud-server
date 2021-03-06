"""
Method to get information about a device type.
"""
from gluon import current


class DeviceType:
    TIMER = 1
    HUB = 2
    SWITCH = 3
    PLUG = 4
    SENSE = 5

    type_names = ['Timer',
                  'uHub',
                  'uSwitch',
                  'uPlug',
                  'uSense']

    def __init__(self, type_id, name, description, device_version, is_input_device, is_output_device, image, icon):
        self.id = type_id
        self.name = name
        self.description = description
        self.device_version = device_version
        self.is_input_device = is_input_device
        self.is_output_device = is_output_device
        self.image = image
        self.icon = icon

    @staticmethod
    def get_device_types():
        """
        Returns list of all device types.
        """
        db = current.db
        device_types = []
        for device_type in db().select(db.device_type.ALL):
            device_types.append(DeviceType(device_type.id, device_type.name, device_type.description,
                                           device_type.device_version, device_type.is_input_device,
                                           device_type.is_output_device,
                                           device_type.image, device_type.icon))
        return device_types

    @staticmethod
    def get_device_type_id(device_type_name):
        """
        Returns device_type id for the given type name.
        """
        index = DeviceType.type_names.index(device_type_name)
        if index >= 0:
            return index + 1

        return ''


    @staticmethod
    def get_device_type_name(device_type_id):
        """
        Returns type name for the given device type id.
        """
        return DeviceType.type_names[device_type_id - 1]