"""
This module takes care of pushing messages to the client
"""

import PubNub
from Action import Action
from Device import Device
from Hub import Hub
import PlugZExceptions

#todo - Remove hardcoded keys
pubnub = PubNub.Pubnub(publish_key='pub-c-9ff29ff2-1427-4864-bbfa-7d3270a233dc',
                       subscribe_key='sub-c-7e20413a-8d2d-11e3-ae86-02ee2ddab7fe',
                       ssl_on=False)


def _push_to_device(device_id, message):
    """
    Publishes given messages to the device.
    Since we don't have direct communication to any device, find the associated hub and send to it.
    """
    device = Device.load(device_id)
    if device is None or device.hub_id is None:
        raise PlugZExceptions.NotFoundError('Device not found.')

    channel = Hub.get_channel(device.hub_id)
    if channel is None:
        raise PlugZExceptions.NotConnectedError('Hub not connected.')

    info = pubnub.publish({
        'channel': channel,
        'message': message
    })


def publish_value_change(device_id, new_value):
    """
    Notify hub that an user wanted to change value of a device
    """
    message = {
        'device_id': device_id,
        'value': new_value
    }
    _push_to_device(device_id, message)


def publish_action_execute(action_id):
    """
    Notify hub that user wanted to execute an action
    """

    message = {
        'action_id': action_id
    }

    # We need to find the hub - for that find the device associated with the action
    action = Action.load(action_id)
    if action is None:
        raise PlugZExceptions.NotFoundError('Action not found.')

    _push_to_device(action.device_id, message)
