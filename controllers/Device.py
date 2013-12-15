class Device:
    """ Registers a device
    """
    def RegisterDevice(DeviceType, Identification, Profile, Hub, Name, Appliance=None):
        raise
    
    """ Fetches a device from database
    """
    def GetDevice(DeviceID):
        raise
        
    """ Fetches all devices associated with a user.
        If DeviceType is provided then the result will be filtered to contain only that type of devices.
    """
    def GetAllDevice(Profile, DeviceType=None):
        raise
