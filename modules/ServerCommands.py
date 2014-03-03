"""
Enum of supported commands - This class used in both plugz-backend and plugz-hub.
If you modify this file copy it in the other project also.
"""


class ServerCommands:
    """
    Change value of a device - Such as Turn on light, Set LED color to #23434 etc
    Arguments:
        device_id - which device's value should be changed.
        value - value to be set.

    Response:
        Yet to define the ACK mechanism.
    """
    SET_DEVICE_STATUS = 0

    """
    Get status of a device - Such as Light, LED, etc
    Arguments:
        device_id - which device's value should be reported.

    Response:
        Once this command is received the hub will update the status of the device through a REST call.
    """
    GET_DEVICE_STATUS = 1

    """
    Execute an action specified by the user
    Arguments:
        action_id - which action should be executed.

    Response:
        Yet to define the ACK mechanism.
    """
    EXECUTE_ACTION = 2

    """
    Channel timeout and server is not going to use this channel anymore for notification.
    Arguments:
        None.

    Response:
        None.
    """
    RECONNECT = 3

