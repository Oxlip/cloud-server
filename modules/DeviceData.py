""" DeviceData is activity information
"""

from gluon import current
from datetime import date


class DeviceData:
    def __init__(self, device_id=None, activity_date=None, output_value=None, time_range=None):
        self.id = None
        self.device_id = device_id
        self.output_value = output_value
        self.activity_date = activity_date
        self.time_range = time_range

    def save(self):
        """
        Saves the current device information
        :return:
        """
        db = current.db
        if self.id:
            db.DeviceData(self.id).update(DeviceId=self.device_id,
                                          OutputValue=self.output_value,
                                          ActivityDate=self.activity_date,
                                          TimeRange=self.time_range
            )
        else:
            self.id = db.DeviceData.insert(DeviceId=self.device_id,
                                           OutputValue=self.output_value,
                                           ActivityDate=self.activity_date,
                                           TimeRange=self.time_range
            )

        return self.id

    @staticmethod
    def get_device_data(device_id, max_days=1):
        """
        Returns list of DeviceData associated with this device.
        If MaxDays is specified then it returns only records created in the last few days(specified by MaxDays).
        :param device_id:
        :param max_days:
        :return:
        """
        db = current.db
        latest_date = date.today() - max_days
        records = current.db(db.DeviceData.DeviceId == device_id and db.DeviceData.ActivityDate > latest_date)
        result = []
        for rec in records:
            new_device_data = DeviceData(rec.DeviceId, rec.ActivityDate, rec.OutputValue, rec.TimeRange)
            new_device_data.id = device_id
            result.append(new_device_data)

        return result