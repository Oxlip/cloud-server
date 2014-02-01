"""
REST API v1
"""
from modules.PlugZExceptions import *
from modules.Device import Device
from modules.DeviceType import DeviceType
from modules.Profile import Profile

@request.restful()
def v1():
    def GET(*args, **vars):
        request.extension = 'json'
        return get_api_dispatch(args, vars)

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


def get_api_dispatch(args, vars):
    if args is None or len(args) == 0:
        return None

    if args[0] == 'user':
        return get_user(args[1:], vars)
    elif args[1] == 'device':
        return get_device(args, vars)

    return None


def get_user(args, vars):
    if args is None or len(args) == 0:
        return None

    user_name = args[0]

    profile = Profile.get_user(user_name)
    return {'first': profile.first_name,
            'last': profile.last_name,
            'contact_info': profile.get_user_contact_info(),
            'args': args,
            'vars': vars}


def get_device(args, vars):
    return {'args': args, 'vars' : vars}