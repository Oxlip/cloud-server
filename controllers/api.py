"""
REST API v1
"""
from modules.PlugZExceptions import *
from modules.Device import Device
from modules.DeviceType import DeviceType
from modules.Profile import Profile
from modules.DeviceData import DeviceData
import PubNub

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
        """
        Handler for POST calls
        """
        request.extension = 'json'
        if args is None or len(args) == 0:
            raise HTTP(406)

        if args[0] == 'user':
            return post_user(args[1:], vars)
        elif args[0] == 'device':
            return post_device(args[1:], vars)

        raise HTTP(406)

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
    Main handler for GET REST api starting /user URL
    """
    if args is None or len(args) == 0:
        raise HTTP(406)

    user_name = args[0]
    try:
        profile = Profile.get_user(user_name)
    except NotFoundError:
        raise HTTP(404)

    if len(args) == 1:
        # /user/{username}
        return get_user_dict(profile)

    if args[1] == 'devices':
        # /user/{username}/devices
        return get_user_devices_dict(profile)

    if args[1] == 'activity':
        # /user/{username}/devices
        return get_user_devices_dict(profile)

    raise HTTP(404)


def post_user(args, vars):
    """
    Main handler for POST REST api starting /user URL
    """
    if args is None or len(args) == 0:
        raise HTTP(406)

    user_name = args[0]
    try:
        profile = Profile.get_user(user_name)
    except NotFoundError:
        raise HTTP(404)

    if args[1] == 'activity':
        # /user/{username}/activity
        ## Initiate Class
        pubnub = PubNub.Pubnub(publish_key='pub-c-9ff29ff2-1427-4864-bbfa-7d3270a233dc',
                               subscribe_key='sub-c-7e20413a-8d2d-11e3-ae86-02ee2ddab7fe',
                               ssl_on=False)
        ## Publish Example
        info = pubnub.publish({
            'channel':  'my_channel',
            'message': {
                'device_id': vars['action_id'],
                'value_changed': 100
            }
        })
        return {'result': 'ok for now'}

    raise HTTP(404)


def get_device(args, vars):
    """
    Main handler for GET REST api starting /device URL
    """
    if args is None or len(args) == 0:
        raise HTTP(406)

    device_id = args[0]
    try:
        device = Device.load(device_id)
    except NotFoundError:
        raise HTTP(404)

    if len(args) == 1:
        # /device/{device_id}
        return get_device_dict(device)

    raise HTTP(404)


def post_device(args, vars):
    """
    Main handler for POST REST api starting /device URL
    """
    if args is None or len(args) == 0:
        raise HTTP(406)

    device_id = args[0]
    try:
        device = Device.load(device_id)
    except NotFoundError:
        raise HTTP(404)

    if len(args) == 1:
        # /device/{device_id} create new device
        pass

    action = args[1]
    if action == 'activity':
        if 'timestamp' not in vars or 'value' not in vars or 'time_range' not in vars:
            raise HTTP(406)
        timestamp = vars['timestamp']
        value = vars['value']
        time_range = vars['time_range']
        d = DeviceData(device_id, timestamp, value, time_range)
        d.save()
        return {}

    raise HTTP(404)
