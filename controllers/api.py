"""
REST API v1
"""
from modules.PlugZExceptions import *
from modules.Device import Device
from modules.DeviceType import DeviceType
from modules.Profile import Profile

@request.restful()
def v1():
    """
    Main handler for Version 1 REST API.
    """
    def GET(*args, **vars):
        """
        Handler for GET calls
        """
        request.extension = 'json'
        if args is None or len(args) == 0:
            return failure_message('Wrong path', args, vars)

        if args[0] == 'user':
            return get_user(args[1:], vars)
        elif args[0] == 'device':
            return get_device(args[1:], vars)

        return failure_message('Unsupported URL', args, vars)

    def POST(*args, **vars):
        request.extension = 'json'
        return dict()

    def PUT(*args, **vars):
        request.extension = 'json'
        return dict()

    def DELETE(*args, **vars):
        request.extension = 'json'
        return dict()

    return locals()

def failure_message(msg, args, vars):
    """
    Prepares failure message.
    """
    return {
        'failure_msg': msg,
        'args': args,
        'vars': vars
    }

def get_device_dict(device):
    """
    Returns an device information as a dictionary.
    """
    return {
        'id': device.id,
        'name': device.name,
        'group': '',
        'type': device.device_type_id,
        'images': []
    }


def get_user_dict(profile):
    """
    Returns user information as a dictionary
    """
    return {
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'email': profile.email
    }


def get_user_devices_dict(profile):
    """
    Returns all devices associated with an user as a dict
    """
    devices = []
    for device in Device.get_devices_for_user(profile.profile_id):
        devices.append(get_device_dict(device))

    return {'devices': devices}


def get_user(args, vars):
    """
    Main handler for user all REST api starting /user URL
    """
    if args is None or len(args) == 0:
        return failure_message('Invalid request', args, vars)

    user_name = args[0]
    profile = Profile.get_user(user_name)

    if len(args) == 1:
        # /user/{username}
        return get_user_dict(profile)

    if args[1] == 'devices':
        # /user/{username}/devices
        return get_user_devices_dict(profile)

    return failure_message('Not supported', args, vars)


def get_device(args, vars):
    """
    Main handler for user all REST api starting /device URL
    """
    if args is None or len(args) == 0:
        return failure_message('Invalid request', args, vars)

    device_id = args[0]
    device = Device.load(device_id)
    if len(args) == 1:
        # /device/{device_id}
        return get_device_dict(device)

    return failure_message('Not supported', args, vars)


