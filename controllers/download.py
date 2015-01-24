""" Controller to manager firmware downloads.
"""


def firmware():
    """
    Return latest firmware for requested device.
    HTTP Arguments:
        dt - Device type (aura, lyra etc)
        hw - Hardware version (v1, ev, dk)

    Example usage:
       wget "http://nuton.in/download/firmware?dt=aura&hw=v1"

    :return: Firmware file as octet stream.
    """
    import os
    device_type = request.vars['dt']
    hardware_version = request.vars['hw']

    try:

        path_prefix = os.path.join(request.folder, 'downloads', 'firmware')
        config_path = os.path.join(path_prefix, 'firmwares.json')
        config_json = open(config_path, 'r').read()

        import gluon.contrib.simplejson
        config_data = gluon.contrib.simplejson.loads(config_json)
        firmware_config = config_data[device_type][hardware_version]
        firmware_path = os.path.join(path_prefix, firmware_config['filename'])
    except:
        raise HTTP(400, 'Invalid request')
    else:
        return response.stream(open(firmware_path, 'rb'), filename=device_type)
