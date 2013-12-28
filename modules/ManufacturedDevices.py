# -*- coding: utf-8 -*-

"""
All devices should be inserted into the ManufacturedDevices table before shipping to the customer.
This class provides a insert method to accomplish that.

TODO - May be we need an delete() method later.
"""

from gluon import current
from PlugZExceptions import AlreadyExistsError


class ManufacturedDevices:
    def __init__(self):
        pass

    @staticmethod
    def insert(identification, device_type_id, date_of_manufacturing=None):
        """
        Insert a new device into the ManufacturedDevice table.
        On error, raises AlreadyExistsError.
        """

        db = current.db

        # If the device already exists raise an exception.
        if db(db.ManufacturedDevices.Identification == identification).count() > 0:
            raise AlreadyExistsError('Another device is already has the same identification- {id}.'.format(id=identification))

        db.ManufacturedDevices.insert(Identification=identification,
                                      DeviceTypeId=device_type_id,
                                      DateOfManufacturing=date_of_manufacturing
                                      )
