"""
All user/profile related functions.
"""
import PlugZExceptions
from applications.backend.modules.Device import Device
from applications.backend.modules.DeviceType import DeviceType

def login():
    """
    Let the user login to his account
    """
    #For debugging only - user 1 is always in.
    session.user_id = 1
    session.user_name = 'Samuel'
    if session.user_id:
        # User is already logged in, lets redirect him to the dashboard.
        return dashboard()

    # write code for facebook/google signin
    return


def logout():
    """
    Let the user logout of his account
    """
    session.user_id = None
    session.forget()


def signup():
    """
    Signup using OAuth providers
    """
    # write facebook/google signup code
    return


def dashboard():
    """
    Landing page for the user after he login.
    """
    response.view = 'dashboard.html'
    devices = Device.get_devices_for_user(session.user_id)
    #TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(devices=devices, device_types=device_types)
