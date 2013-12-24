from gluon import current

""" Module to control device objectsss.
"""
class Device:
    """ Initializes device fields with given information.
    """
    def __init__(self, DeviceType = None, Identification = None, Profile = None, Hub = None, Name = None, RegisteredDate = None, DefaultValue = None, Appliance = None):
        self.Id = None
        self.DeviceType = DeviceType
        self.Identification = Identification
        self.Profile = Profile
        self.Hub = Hub
        self.Name = Name
        self.RegisteredDate = RegisteredDate
        self.DefaultValue = DefaultValue
        self.Appliance = Appliance
    
    """ Loads device information from the database into current object.
    
        If the device is not found then raises an exception.
    """
    def Load(self, DeviceId):
        device = current.db.Device(DeviceId)
        if device == None:
            # TODO - define exception.
            raise
        
        if device.isDeleted:
            # TODO - define exception.
            raise

        self.DeviceId = device.DeviceId
        self.DeviceType = device.DeviceType
        self.Identification = device.Identification
        self.Profile = device.Profile
        self.Hub = device.Hub
        self.Name = device.Name
        self.RegisteredDate = device.RegisteredDate
        self.DefaultValue = device.DefaultValue
        self.Appliance = device.Appliance
        
        return True
    
    """ Saves the current device.
    
        On success returns the newly created deviceId.
    """
    def Save(self):
        db = current.db
        #Check whether need to create a new record OR update existing record.
        if (self.Id):
            db.Device(self.Id).update(DeviceType = self.DeviceType,
                                      Identification = self.Identification,
                                      Profile = self.Profile,
                                      Hub = self.Hub,
                                      Name = self.Name,
                                      RegisteredDate = self.RegisteredDate,
                                      DefaultValue = self.DefaultValue,
                                      Appliance = self.Appliance
                                      )
        else:
            self.Id = db.Device.insert(DeviceType = self.DeviceType,
                                       Identification = self.Identification,
                                       Profile = self.Profile,
                                       Hub = self.Hub,
                                       Name = self.Name,
                                       RegisteredDate = self.RegisteredDate,
                                       DefaultValue = self.DefaultValue,
                                       Appliance = self.Appliance
                                       )

        return self.Id
        
    
    """ Deletes current device.
    
        On failure such as when the deviceId is not found raises an exception.
    """
    @staticmethod
    def Delete(DeviceId):
        # For now we mark only the device as deleted, later we may need to modify the DeviceData and Action tables. 
        current.db(db.Device.id == DeviceId).update(isDeleted=True)
    
