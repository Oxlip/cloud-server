# -*- coding: utf-8 -*-

"""
All device related work is controlled by this file.
"""

from modules.ManufacturedDevices import ManufacturedDevices
from modules.PlugZExceptions import *
from datetime import datetime


def manufactured():
    """
    Add a newly manufactured device.
    """
    form = FORM(TABLE(
                TR(TD(LABEL('Identification :')), TD(INPUT(_name='Identification', requires=IS_NOT_EMPTY()))),
                TR(TD(LABEL('Type :')), TD(INPUT(_name='DeviceType', requires=IS_NOT_EMPTY()))),
                TR(TD(INPUT(_type='submit')))
            ))
    if not form.process().accepted:
        return dict(form=form)

    # Try to insert the device
    try:
        ManufacturedDevices.insert(identification=form.vars.Identification, device_type_id=form.vars.DeviceType,
                                   date_of_manufacturing=datetime.today())
    except AlreadyExistsError:
        return 'The given serial number already exists.'
    else:
        return 'Successfully added the device.'

