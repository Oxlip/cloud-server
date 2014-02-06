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
            raise HTTP(406)

        if args[0] == 'user':
            return get_user(args[1:], vars)
        elif args[0] == 'device':
            return get_device(args[1:], vars)

        raise HTTP(406)

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
        raise HTTP(406)

    user_name = args[0]
    try:
        profile = Profile.get_user(user_name)
    except NotFoundError:
        raise HTTP(400)

    if len(args) == 1:
        # /user/{username}
        return get_user_dict(profile)

    if args[1] == 'devices':
        # /user/{username}/devices
        return get_user_devices_dict(profile)

    raise HTTP(404)


def get_device(args, vars):
    """
    Main handler for user all REST api starting /device URL
    """
    if args is None or len(args) == 0:
        raise HTTP(406)

    device_id = args[0]
    try:
        device = Device.load(device_id)
    except NotFoundError:
        raise HTTP(400)

    if len(args) == 1:
        # /device/{device_id}
        return get_device_dict(device)

    raise HTTP(404)


