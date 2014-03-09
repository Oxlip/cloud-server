"""
All user/profile related functions.
"""
import PlugZExceptions
import requests


def dashboard():
    """
    Landing page for the user - shows user devices and energy usage etc
    """

    # if user has not logged in, redirect to login page
    if session.user_name is None:
        return login()

    from applications.backend.modules.Device import Device
    from applications.backend.modules.DeviceType import DeviceType

    response.view = 'dashboard.html'
    devices = Device.get_devices_for_user(session.user_id)
    #TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(devices=devices, device_types=device_types)


def login():
    """
    Login through social login using janrain
    """
    response.view = 'login.html'
    return dict()


def login_redirect():
    """
    janrain will redirect to this controller once login was successful.
    """

    # janrain will send a one time token.
    # use the token to make REST request to janrain to get profile details.
    api_params = {
        'token': request.post_vars['token'],
        'apiKey': '528f00c316b91171a90e391c8ea0af44796770f6',
        'format': 'json',
    }
    r = requests.post('https://rpxnow.com/api/v2/auth_info', params=api_params)
    if r.status_code != requests.codes.ok:
        raise HTTP(503)

    json_result = r.json()
    json_profile = json_result['profile']

    from applications.backend.modules.Profile import Profile
    if 'givenName' in json_profile['name']:
        first_name = ['givenName']
        last_name = json_profile['name']['familyName']
    else:
        names = json_profile['name']['formatted'].split(' ')
        first_name = names[0]
        last_name = names[-1]

    email = json_profile['email']
    if 'preferredUsername' in json_profile:
        username = json_profile['preferredUsername']
    else:
        #TODO - some providers(such as yahoo) does not have username concept, we should handle it correctly
        #for now I am joining the first name and last name
        username = '{first}_{last}'.format(first=first_name.lower(), last=last_name.lower())
    photo = json_profile['photo']
    identifier = json_profile['identifier']

    # if the user is signing in for first time, register them
    if not Profile.is_email_registered(email):
        #TODO - add custom field in janrain to capture shipping address but that requires PRO account so for now....
        #TODO - handle registration failure
        Profile.register_profile(username=username, first_name=first_name, last_name=last_name, email=email,
                                 photo=photo, identifier=identifier)

    session.user_name, session.user_session_id, session.user_id = Profile.login(email)

    return dashboard()


def logout():
    """
    Let the user logout of his account
    """
    session.user_name = None
    session.user_session_id = None
    session.user_id = None
    session.forget()

