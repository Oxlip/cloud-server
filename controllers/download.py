""" Controller to manager firmware downloads.
"""
import os
import gluon.contrib.simplejson


def get_firmware_info():
    """
    Return latest firmware info for requested device.
    HTTP Arguments:
        dt - Device type (aura, lyra etc)
        hw - Hardware version (v1, ev, dk)

    Example usage:
       wget "http://nuton.in/download/get_firmware_info?dt=aura&hw=v1"

    :return: Firmware info as json.
    """
    try:
        device_type = request.vars['dt']
        hardware_version = request.vars['hw']
    except:
        raise HTTP(400, 'Bad parameter')

    try:
        path_prefix = os.path.join(request.folder, 'downloads', 'firmware')
        config_path = os.path.join(path_prefix, 'firmwares.json')
        config_json = open(config_path, 'r').read()

        config_data = gluon.contrib.simplejson.loads(config_json)
        firmware_config = config_data[device_type][hardware_version]
    except:
        raise HTTP(400, 'Invalid request')

    del firmware_config['filename']
    return gluon.contrib.simplejson.dumps(firmware_config)

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

    try:
        device_type = request.vars['dt']
        hardware_version = request.vars['hw']
    except:
        raise HTTP(400, 'Bad parameter')

    try:
        path_prefix = os.path.join(request.folder, 'downloads', 'firmware')
        config_path = os.path.join(path_prefix, 'firmwares.json')
        config_json = open(config_path, 'r').read()

        config_data = gluon.contrib.simplejson.loads(config_json)
        firmware_config = config_data[device_type][hardware_version]
        firmware_path = os.path.join(path_prefix, firmware_config['filename'])

    except:
        raise HTTP(400, 'Invalid request')
    else:
        return response.stream(open(firmware_path, 'rb'), filename=device_type)


def update_firmware():
    """
    Hacky interface to update the latest firmware information.
    After uploading the firmware, scripts can use this interface to update the JSON file.

    TODO - This interface should be removed after development.

    HTTP Arguments:
        dt - Device type (aura, lyra etc)
        hw - Hardware version (v1, ev, dk)
        filename - Name of the binary.
        fw_date - timestamp of the firmware.
        release_notes - Any notes about this release.

    Example usage:
       curl "http://nuton.in/download/firmware?dt=aura&hw=v1&filename=aura_s110.bin&fw_date=03Feb2015_10:30"

    """

    try:
        device_type = request.vars['dt']
        hardware_version = request.vars['hw']
        firmware_filename = request.vars['filename']
        fw_date = request.vars['fw_date']
        release_notes = request.vars['release_notes']
    except:
        raise HTTP(400, 'Bad parameter')

    try:
        path_prefix = os.path.join(request.folder, 'downloads', 'firmware')
        config_path = os.path.join(path_prefix, 'firmwares.json')
        config_json = open(config_path, 'r').read()

        config_data = gluon.contrib.simplejson.loads(config_json)
        config_data[device_type][hardware_version]['filename'] = firmware_filename
        config_data[device_type][hardware_version]['fw_date'] = fw_date
        config_data[device_type][hardware_version]['release_notes'] = release_notes
        gluon.contrib.simplejson.dump(config_data, open(config_path, 'w'))
    except:
        raise HTTP(400, 'Invalid request')
    else:
        return 'Success'
