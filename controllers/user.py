"""
All user/profile related functions.
"""
import PlugZExceptions


def login():
    """
    Let the user login to his account
    """
    from Profile import Profile

    if session.user_name is None:
        # TODO - write code for facebook/google signin

        # TODO - Remove this hardcoded value
        session.user_name, session.user_session_id, session.user_id = Profile.login('samueldotj@gmail.com')

    if session.user_name is None:
        raise HTTP(405)

    return dashboard()


def logout():
    """
    Let the user logout of his account
    """
    session.user_name = None
    session.user_session_id = None
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
    from applications.backend.modules.Device import Device
    from applications.backend.modules.DeviceType import DeviceType

    response.view = 'dashboard.html'
    devices = Device.get_devices_for_user(session.user_id)
    #TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(devices=devices, device_types=device_types)
