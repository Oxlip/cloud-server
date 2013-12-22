""" Module to control device objects.
"""
class Device:
    def __init__(self, DeviceType = None, Identification = None, Profile = None, Hub = None, Name = None, RegisteredDate = None, DefaultValue = None, Appliance = None):
        self.DeviceType = DeviceType
        self.Identification = Identification
        self.Profile = Profile
        self.Hub = Hub
        self.Name = Name
        self.RegisteredDate = RegisteredDate
        self.DefaultValue = DefaultValue
        self.Appliance = Appliance
    
    """ Loads device information from the database into current object.
    """
    def Load(self, DeviceId):
        raise
    
    """ Saves the current device.
    """
    def Save(self):
        raise
    
    """ Deletes current device.
    """
    def Delete(self):
        raise
    
    """ Adds a new DeviceData record based on the given data.
        Returns the newly added DeviceData. 
    """
    def AddDeviceData(self, ActivityTime, OutputValue, TimeRange):
        raise

    """ Returns list of DeviceData associated with this device
        If MaxDays is specified then it returns only records created in the last few days(sepcified by MaxDays).
    """
    def GetDeviceData(self, MaxDays=1):
        raise
    
    """ Returns list of actions associated with the current device. 
    """
    def GetActions(self):
        raise