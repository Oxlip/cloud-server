"""
This module takes care of pushing messages to the client
"""

import PubNub
from Device import Device
import PlugZExceptions

#todo - Remove hardcoded keys
pubnub = PubNub.Pubnub(publish_key='pub-c-9ff29ff2-1427-4864-bbfa-7d3270a233dc',
                       subscribe_key='sub-c-7e20413a-8d2d-11e3-ae86-02ee2ddab7fe',
                       ssl_on=False)


def publish_device_value_change(device_id, new_value):
    """
    Notify hub that user wanted to change value of a device
    """
    device = Device.load(device_id)
    if device is None or device.hub_id is None:
        raise PlugZExceptions.NotFoundError('Device not found.')

    channel = Device.get_hub_publish_channel(device.hub_id)
    if channel is None:
        raise PlugZExceptions.NotConnectedError('Hub not connected.')

    info = pubnub.publish({
        'channel': channel,
        'message': {
            'device_id': device_id,
            'value': new_value
        }
    })


def publish_action_execute(action_id):
    """
    Notify hub that user wanted to execute an action
    """

    # We need to find the hub - for that find the device associated with the action
    action = Action.load(action_id)
    if action is None:
        raise PlugZExceptions.NotFoundError('Action not found.')

    device = Device.load(action.device_id)
    if device is None:
        raise PlugZExceptions.NotFoundError('Device not found.')

    channel = Device.get_hub_publish_channel(device.hub_id)
    if channel is None:
        raise PlugZExceptions.NotConnectedError('Hub not connected.')

    info = pubnub.publish({
        'channel': channel,
        'message': {
            'action_id': action_id
        }
    })
