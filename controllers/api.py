"""
REST API v1
"""
from applications.backend.modules.Device import Device
from applications.backend.modules.Hub import Hub
from applications.backend.modules.DeviceType import DeviceType
from applications.backend.modules.Profile import Profile
from applications.backend.modules.DeviceData import DeviceData
import PlugZExceptions
import PushNotification

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
        response.generic_patterns = ['*.json']
        if args is None or len(args) == 0:
            raise HTTP(406)

        if args[0] == 'user':
            return get_user(args[1:], vars)
        elif args[0] == 'device':
            return get_device(args[1:], vars)
        elif args[0] == 'hub':
            return get_hub(args[1:], vars)

        raise HTTP(406)

    def POST(*args, **vars):
        """
        Handler for POST calls
        """
        request.extension = 'json'
        response.generic_patterns = ['*.json']
        if args is None or len(args) == 0:
            raise HTTP(406)

        if args[0] == 'user':
            return post_user(args[1:], vars)
        elif args[0] == 'device':
            return post_device(args[1:], vars)
        elif args[0] == 'hub':
            return post_hub(args[1:], vars)

        raise HTTP(406)

    def PUT(*args, **vars):
        request.extension = 'json'
        response.generic_patterns = ['*.json']
        return dict()

    def DELETE(*args, **vars):
        request.extension = 'json'
        response.generic_patterns = ['*.json']
        return dict()

    return locals()


def get_device_dict(device):
    """
    Returns a device information as a dictionary.
    """
    return {
        'id': device.id,
        'name': device.name,
        'group': '',
        'type': device.device_type_id,
        'images': []
    }


def get_hub_devices_dict(hub_id):
    """
    Returns all devices associated with an hub as a dict
    """
    devices = []
    for device in Hub.get_devices(hub_id):
        devices.append(get_device_dict(device))

    return {'devices': devices}


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


def hub_connect_result_as_dict(hub_identification, authentication_key):
    """
    Establishes a hub session and returns channel
    """
    hub_id, channel = Hub.connect(hub_identification, authentication_key)
    return {
        'id': hub_id,
        'channel': channel
    }


def get_user(args, vars):
    """
    Main handler for GET REST api starting /user URL
    """
    if args is None or len(args) == 0:
        raise HTTP(406)

    user_name = args[0]
    try:
        profile = Profile.get_user(user_name)
    except PlugZExceptions.NotFoundError:
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
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    if args[1] == 'activity':
        # /user/{username}/activity
        if 'device_id' in vars and 'value' in vars:
            profile.record_device_value_changed(long(vars['device_id']), value = vars['value'])
        elif 'action_id' in vars:
            profile.record_action_executed(vars['action_id'])
        else:
            raise HTTP(400)

        return {'result': result}

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
    except PlugZExceptions.NotFoundError:
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
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    if len(args) == 1:
        # /device/{device_id} create new device
        return HTTP(406)

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


def get_hub(args, vars):
    """
    Main handler for GET REST api starting /hub URL
    """
    if args is None or len(args) == 0:
        raise HTTP(406)

    hub_identification = args[0]
    try:
        hub = Hub.load_by_identification(hub_identification)
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    if len(args) == 1:
        # /hub/{identification} is not supported
        return HTTP(406)

    if args[1] == 'devices':
        # /hub/{identification}/devices
        return get_hub_devices_dict(hub.id)

    raise HTTP(404)


def post_hub(args, vars):
    """
    Main handler for POST REST api starting /hub URL
    """
    if args is None or len(args) == 0:
        raise HTTP(406)

    hub_identification = args[0]

    if len(args) == 1:
        # /hub/{identification} is not acceptable
        return HTTP(406)

    if args[1] == 'connect':
        # /hub/{identification}/connect - create new connection
        return hub_connect_result_as_dict(hub_identification, request.env['http_auth_key'])
