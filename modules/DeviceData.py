from gluon import current
from datetime import date 

""" DeviceData is activity information
"""
class DeviceData:
    def __init__(self, DeviceId=None, ActivityDate=None, OutputValue=None, TimeRange=None):
        self.Id = None
        self.DeviceId = DeviceId
        self.OutputValue = OutputValue
        self.ActivityDate = ActivityDate
        self.TimeRange = TimeRange
    
    """ Saves the current device information
    """
    def Save(self):
        db = current.db
        if (self.Id):
            db.DeviceData(self.Id).update(DeviceId = self.DeviceId,
                                          OutputValue = self.OutputValue,
                                          ActivityDate = self.ActivityDate,
                                          TimeRange = self.TimeRange
                                          )
        else:
            self.Id = db.DeviceData.insert(DeviceId = self.DeviceId,
                                           OutputValue = self.OutputValue,
                                           ActivityDate = self.ActivityDate,
                                           TimeRange = self.TimeRange
                                           )

        return self.Id
    
    """ Returns list of DeviceData associated with this device.
        If MaxDays is specified then it returns only records created in the last few days(sepcified by MaxDays).
    """
    @staticmethod
    def GetDeviceData(DeviceId, MaxDays=1):
        db = current.db
        latest_date = date.today() - MaxDays
        records = current.db(db.DeviceData.DeviceId == DeviceId and db.DeviceData.ActivityDate > latest_date )
        result = []
        for rec in records:
            new_devicedata = DeviceData(DeviceId=rec.DeviceId, ActivityDate=rec.ActivityDate, OutputValue=rec.OutputValue, TimeRange=rec.TimeRange)
            new_devicedata.Id = DeviceId
            result.append(new_devicedata)
            
        return result