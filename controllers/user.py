"""
All user/profile related functions.
"""
import requests
import string
import random
import CloudServerExceptions
from Device import Device
from DeviceType import DeviceType
from Profile import Profile


def dashboard():
    """
    Landing page for the user - shows user devices and energy usage etc
    """

    # if user has not logged in, redirect to login page
    if session.user_name is None:
        return login()

    response.view = 'dashboard.html'
    devices = Device.get_devices_for_user(session.user_id)
    # TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    try:
        profile = Profile.get_user(session.user_name)
    except CloudServerExceptions.NotFoundError:
        session.user_name = None
        return 'User name not found'

    return dict(profile=profile, devices=devices, device_types=device_types)


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

    return dashboard()


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
    Controller for Statistics page - shows user devices and energy usage etc
    """

    # if user has not logged in, redirect to login page
    if session.user_name is None:
        return login()

    response.view = 'Statistics.html'
    devices = Device.get_devices_for_user(session.user_id)
    # TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(profile=Profile.get_user(session.user_name), devices=devices, device_types=device_types)


def rule():
    """
    Rule - controller to manage rule.
    """

    # if user has not logged in, redirect to login page
    if session.user_name is None:
        return login()

    response.view = 'rule.html'
    devices = Device.get_devices_for_user(session.user_id)
    # TODO - devicetypes wont change so make them available as global
    device_types = DeviceType.get_device_types()
    return dict(profile=Profile.get_user(session.user_name), devices=devices, device_types=device_types)


def register_device():
    _error_message = ""
    if not (request.vars.txtSerialNo and request.vars.txtdeviceName):
        response.flash = T("Enter a Valid Serial No or Device Name")
        return

    try:
        from DeviceType import DeviceType
        device_type_id = DeviceType.get_device_type_id(request.vars.lstDeviceType)
    except:
        return DIV('Error registering device.')

    hub_id = request.vars.txtHubId.strip()
    if hub_id == '':
        hub_id = None

    new_device = Device.register(serial_no=request.vars.txtSerialNo, device_type_id=device_type_id,
                                 profile_id=session.user_id, device_name=request.vars.txtdeviceName,
                                 hub_id=hub_id)

    if not new_device:
        _error_message = "Error Adding Device. Check for Serial Number"
        response.flash = _error_message


    scriptTag = SCRIPT("$('.switch-mini').bootstrapSwitch(); $('#fafaAddDevice').click();" if not _error_message
                       else ("$('.switch-mini').bootstrapSwitch(); alert('" + _error_message + "');"))

    devices = Device.get_devices_for_user(session.user_id)
    return CAT(scriptTag,
               *[DIV(
                   DIV(IMG(_src=URL('static/images/device_icons', device.get_image())), _class="col-md-2"),
                   DIV(device.name, _class="col-md-2"),
                   DIV(INPUT(_type="checkbox", _class="switch-mini"), _class="col-md-2"),
                   _class="row") for device in devices])
    # DIV(DIV(DIV(SPAN("ON", _class="switch-left switch-info"), LABEL(_for)),
    # _class="has-switch switch-animate switch-mini switch-on"), _class="col-md-5"),


def add_rule():
    _error_message = ""
    if not request.vars.ruleexpression:
        response.flash = T("Please fill All fields.")

    from Condition import Condition
    from Action import Action

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
        raise CloudServerExceptions.DatabaseError('Error updateing Rule')

    rule_id = Condition.add_rule(None, session.user_id, rule_name, master_condition, master_action)
    Condition.publish_rule_to_hub(session.user_id, rule_id, request.vars.ruleexpression)

    return True


def _random_serial(length=10):
    """
    Returns random serial number with given length
    """
    chars = string.ascii_uppercase + string.digits
    return ''.join(random.choice(chars) for _ in range(length))


def add_random_devices():
    """
    For debugging and testing we need an easy way to add devices. This function does that, we invoked via
     http://servername/user/add_random_devices it creates 3 devices(uSwitch, uPlug and uSense)
    """
    try:
        profile = Profile.get_user(session.user_name)
    except CloudServerExceptions.NotFoundError:
        return 'Invalid username - {0}'.format(session.user_name)

    # Find a hub associated with the user.
    try:
        devices = Device.get_devices_for_user(profile.profile_id)
    except:
        return 'Hub fetch error'
    hub_id = None
    for dev in devices:
        if dev.device_type_id == DeviceType.HUB:
            hub_id = dev.id
            break
    if hub_id is None:
        #No hub is registered.
        hub = Device.register(serial_no=_random_serial(), device_type_id=DeviceType.HUB, profile_id=profile.profile_id,
                              device_name='Hub')
        hub_id = hub.id

    appliance_type_count = db(db.appliance_type).count()

    created_count = 0
    for device_type_id in [DeviceType.SWITCH, DeviceType.SENSE, DeviceType.PLUG]:
        serial = _random_serial()

        #uSwitch would have 4 devices using the same serial number
        if device_type_id == DeviceType.SWITCH:
            device_count = 4
        else:
            device_count = 1
        for i in range(device_count):
            try:
                if device_type_id in [DeviceType.SWITCH, DeviceType.PLUG]:
                    appliance_type_id = random.choice(range(appliance_type_count))
                else:
                    appliance_type_id = None

                Device.register(serial_no=serial, device_type_id=device_type_id, profile_id=profile.profile_id,
                                device_name=serial, hub_id=hub_id, appliance_type_id=appliance_type_id)
            except:
                continue
            created_count += 1


    return '{0} devices created'.format(created_count)
