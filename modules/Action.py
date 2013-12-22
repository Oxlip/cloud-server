""" Simply put an action associates a value with an device.
    It also links multiple actions into one(through MasterAction).
"""
class Action:
    def __init__(self, Name=None, Device=None, OutputValue=None, MasterAction=None):
        self.Name = Name
        self.Device = Device
        self.OutputValue = OutputValue
        self.MasterAction = MasterAction

    """ Saves the current DeviceData.
    """
    def Save(self):
        raise
    
    """ Loads the Action information by using the ActionId provided.
    """
    def Load(self, ActionId):
        raise
    
    """ Adds an action to the given device.
        Returns the newly created action.
    """
    def AddAction(self, DeviceId, Name, OutputValue):
        raise
    
    """ Remove Action
    """
    def Delete(self):
        raise