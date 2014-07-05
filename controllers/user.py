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
    from applications.backend.modules.Profile import Profile

    response.view = 'dashboard.html'
    devices = Device.get_devices_for_user(session.user_id)
    # TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(profile=Profile.get_user(session.user_name), devices=devices, device_types=device_types)


def home():
    """
    Landing page for the user - shows user devices and energy usage etc
    """

    # if user has not logged in, redirect to login page
    if session.user_name is None:
        return login()

    from applications.backend.modules.Device import Device
    from applications.backend.modules.DeviceType import DeviceType
    from applications.backend.modules.Profile import Profile

    response.view = 'home.html'
    devices = Device.get_devices_for_user(session.user_id)
    # TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(profile=Profile.get_user(session.user_name), devices=devices, device_types=device_types)


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
        first_name = json_profile['name']['givenName']
        last_name = json_profile['name']['familyName']
    else:
        names = json_profile['name']['formatted'].split(' ')
        first_name = names[0]
        last_name = names[-1]

    email = json_profile['email']
    if 'preferredUsername' in json_profile:
        username = json_profile['preferredUsername']
    else:
        # TODO - some providers(such as yahoo) does not have username concept, we should handle it correctly
        # for now I am joining the first name and last name
        username = '{first}_{last}'.format(first=first_name.lower(), last=last_name.lower())
    photo = json_profile['photo']
    identifier = json_profile['identifier']

    # if the user is signing in for first time, register them
    if not Profile.is_email_registered(email):
        # TODO - add custom field in janrain to capture shipping address but that requires PRO account so for now....
        # TODO - handle registration failure
        Profile.register_profile(username=username, first_name=first_name, last_name=last_name, email=email,
                                 photo=photo, identifier=identifier)

    session.user_name, session.user_session_id, session.user_id = Profile.login(email)

    return home()


def logout():
    """
    Let the user logout of his account
    """
    session.user_name = None
    session.user_session_id = None
    session.user_id = None
    session.forget()


def statistics():
    """
    Landing page for the user - shows user devices and energy usage etc
    """

    # if user has not logged in, redirect to login page
    if session.user_name is None:
        return login()

    from applications.backend.modules.Device import Device
    from applications.backend.modules.DeviceType import DeviceType
    from applications.backend.modules.Profile import Profile

    response.view = 'Statistics.html'
    devices = Device.get_devices_for_user(session.user_id)
    # TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(profile=Profile.get_user(session.user_name), devices=devices, device_types=device_types)


def manage_rule():
    """
    Landing page for the user - shows user devices and energy usage etc
    """

    # if user has not logged in, redirect to login page
    if session.user_name is None:
        return login()

    from applications.backend.modules.Device import Device
    from applications.backend.modules.DeviceType import DeviceType
    from applications.backend.modules.Profile import Profile

    response.view = 'manage_rule.html'
    devices = Device.get_devices_for_user(session.user_id)
    # TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(profile=Profile.get_user(session.user_name), devices=devices, device_types=device_types)


def manage_device():
    """
    Landing page for the user - shows user devices and energy usage etc
    """

    # if user has not logged in, redirect to login page
    if session.user_name is None:
        return login()

    from applications.backend.modules.Device import Device
    from applications.backend.modules.DeviceType import DeviceType
    from applications.backend.modules.Profile import Profile

    response.view = 'manage_device.html'
    devices = Device.get_devices_for_user(session.user_id)
    # TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(profile=Profile.get_user(session.user_name), devices=devices, device_types=device_types)


def register_device():
    _error_message = ""
    if not (request.vars.txtSerialNo and request.vars.txtdeviceName):
        response.flash = T("Enter a Valid Serial No or Device Name")
        return

    from applications.backend.modules.Device import Device

    new_device = Device.register(request.vars.txtSerialNo, 1, session.user_id, request.vars.txtdeviceName)

    if not new_device:
        response.flash = "Error Adding Device. Check for Serial Number"
        _error_message = "Error Adding Device. Check for Serial Number"

    scriptTag = SCRIPT("$('.switch-mini').bootstrapSwitch(); $('#fafaAddDevice').click();" if not _error_message
                       else ("$('.switch-mini').bootstrapSwitch(); alert('" + _error_message + "');"))

    devices = Device.get_devices_for_user(session.user_id)
    return CAT(scriptTag,
               *[DIV(
                   DIV(IMG(_src=URL('static/images/device_icons', device.get_image())), _class="col-md-2"),
                   DIV(device.name, _class="col-md-5"),
                   DIV(INPUT(_type="checkbox", _class="switch-mini"), _class="col-md-5"),
                   _class="row") for device in devices])
    # DIV(DIV(DIV(SPAN("ON", _class="switch-left switch-info"), LABEL(_for)),
    # _class="has-switch switch-animate switch-mini switch-on"), _class="col-md-5"),


def add_rule():
    _error_message = ""
    if not request.vars.ruleexpression:
        response.flash = T("Please fill All fields.")

    from applications.backend.modules.Condition import Condition
    from applications.backend.modules.Action import Action

    try:
        import json
    except ImportError:
        import simplejson as json

    rule_expression = json.loads(request.vars.ruleexpression)
    conditions = rule_expression['Conditions']
    actions = rule_expression['Actions']

    rule_name = rule_expression['rulename']
    action_name = rule_expression['actionName']

    master_condition = None
    master_action = 0
    for condition in conditions:
        for key, value in condition.items():
            master_condition = Condition.save_condition(key, 1, value, True, master_condition)

    for action in actions:
        for key, value in action.items():
            master_action = Action.save_action(action_name, key, value, master_action)

    if master_action is None or master_condition is None:
        raise PlugZExceptions.ErrorUpdatingPlugzDatabase('Error updateing Rule')

    rule_id = Condition.add_rule(None, session.user_id, rule_name, master_condition, master_action)
    Condition.publish_rule_to_hub(session.user_id, rule_id, request.vars.ruleexpression)

    return True



