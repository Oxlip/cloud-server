# -*- coding: utf-8 -*-

"""
All devices should be inserted into the manufactured_devices table before shipping to the customer.
This class provides a insert method to accomplish that.

TODO - May be we need an delete() method later.
"""

from gluon import current
from PlugZExceptions import AlreadyExistsError


class manufactured_devices:
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
        if db(db.manufactured_devices.identification == identification).count() > 0:
            raise AlreadyExistsError('Another device is already has the same identification- {id}.'.format(id=identification))

        db.manufactured_devices.insert(identification=identification,
                                       device_type_id=device_type_id,
                                       date_of_manufacture=date_of_manufacturing
        )
