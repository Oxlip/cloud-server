"""
REST API v1
"""
from Device import Device
from Hub import Hub
from Profile import Profile
from wheezy.routing import PathRouter

import PlugZExceptions

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


def api_v1_get_user(args, vars):
    """
    GET /user/{username}
    """
    try:
        profile = Profile.get_user(args['username'])
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    return {
        'first_name': profile.first_name,
        'last_name': profile.last_name,
        'email': profile.email
    }


def api_v1_get_user_devices(args, vars):
    """
    GET /user/{username}/devices
    """
    try:
        profile = Profile.get_user(args['username'])
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    devices = []
    for device in Device.get_devices_for_user(profile.profile_id):
        devices.append(get_device_dict(device))

    return {'devices': devices}


def api_v1_get_user_activity(args, vars):
    """
    GET /user/{username}/activity
    """
    try:
        profile = Profile.get_user(args['username'])
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    #TODO - Implement this
    return {'activity': []}


def api_v1_get_device(args, vars):
    """
    GET /device/{device_id}
    """
    try:
        device = Device.load(args['device_id'])
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    return get_device_dict(device)


def api_v1_get_hub_devices(args, vars):
    """
    GET /hub/{identification}/devices
    """
    try:
        hub = Hub.load_by_identification(args['identification'])
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    devices = []
    for device in Hub.get_devices(hub.id):
        devices.append(get_device_dict(device))

    return {'devices': devices}

get_router = PathRouter()
get_router.add_routes([
    ('/user/(?P<username>\w+)', api_v1_get_user),
    ('/user/(?P<username>\w+)/devices', api_v1_get_user_devices),
    ('/user/(?P<username>\w+)/activity', api_v1_get_user_activity),

    ('/device/(?P<device_id>\w+)', api_v1_get_device),

    ('/hub/(?P<identification>\w+)/devices', api_v1_get_hub_devices)
])


def api_v1_post_user_activity(args, vars):
    """
    POST /user/{username}/activity
    """
    try:
        profile = Profile.get_user(args['username'])
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    if 'device_id' in vars and 'value' in vars:
        profile.record_device_value_changed(long(vars['device_id']), vars['value'])
    elif 'action_id' in vars:
        profile.record_action_executed(vars['action_id'])
    else:
        raise HTTP(400)

    return {'result': 'ok'}


def api_v1_post_device_activity(args, vars):
    """
    GET /device/{device_id}/activity
    """
    if 'timestamp' not in vars or 'value' not in vars or 'time_range' not in vars:
        raise HTTP(406)

    try:
        device = Device.load(args['device_id'])
    except PlugZExceptions.NotFoundError:
        raise HTTP(404)

    device.record_value_change(timestamp=vars['timestamp'], value=vars['value'], time_range= vars['time_range'])

    return {'result': 'ok'}


def api_v1_post_hub_connect(args, vars):
    """
    POST /hub/{identification}/connect
    """
    hub_id, channel = Hub.connect(args['identification'], request.env['http_auth_key'])
    return {
        'id': hub_id,
        'channel': channel
    }


post_router = PathRouter()
post_router.add_routes([
    ('/user/(?P<username>\w+)/activity', api_v1_post_user_activity),

    ('/device/(?P<device_id>\w+)/activity', api_v1_post_device_activity),

    ('/hub/(?P<identification>\w+)/connect', api_v1_post_hub_connect)
])

url_prefix = '/{0}/{1}'.format(request.controller, request.function)

@request.restful()
def v1():
    """
    Main handler for Version 1 REST API.
    """
    def GET(*args, **vars):
        request.extension = 'json'
        response.generic_patterns = ['*.json']

        url_path = request.url.split(url_prefix).pop()
        handler, args = get_router.match(url_path)
        if handler is None:
            raise HTTP(404)

        return handler(args, vars)

    def POST(*args, **vars):
        request.extension = 'json'
        response.generic_patterns = ['*.json']

        url_path = request.url.split(url_prefix).pop()
        handler, args = post_router.match(url_path)
        if handler is None:
            raise HTTP(404)

        return handler(args, vars)

    def PUT(*args, **vars):
        request.extension = 'json'
        response.generic_patterns = ['*.json']
        return dict()

    def DELETE(*args, **vars):
        request.extension = 'json'
        response.generic_patterns = ['*.json']
        return dict()

    return locals()

