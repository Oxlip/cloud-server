""" DeviceData is activity information
"""
class DeviceData:
    def __init__(self, Device=None, ActivityTime=None, OutputValue=None, TimeRange=None):
        self.Device = Device
        self.OutputValue = OutputValue
        self.ActivityTime = ActivityTime
        self.TimeRange = TimeRange
    
    """ Saves the current device information
    """
    def Save(self):
        raise
    
    def Load(self, DeviceDataId):
        raise
