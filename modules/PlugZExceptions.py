# -*- coding: utf-8 -*-
"""
Defines custom exceptions and error codes.
"""


class AlreadyExistsError(Exception):
    pass


class NotFoundError(Exception):
    pass


class MarkedAsDeletedError(Exception):
    pass


class InvalidDeviceError(Exception):
    pass


class NotConnectedError(Exception):
    pass
