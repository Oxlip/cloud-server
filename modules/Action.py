""" Simply put an action associates a value with an device.
    It also links multiple actions into one(through MasterAction).
"""

from gluon import current


class Action:
    def __init__(self, action_id=None, name=None, device_id=None, output_value=None, master_action_id=None):
        self.id = action_id
        self.name = name
        self.device_id = device_id
        self.output_value = output_value
        self.master_action_id = master_action_id

    def save(self):
        """
        Saves the current DeviceData.
        On success returns the newly created device_id.

        @return:
        """
        db = current.db
        if self.id:
            db.Actions(self.id).update(Name=self.name,
                                       DeviceId=self.device_id,
                                       OutputValue=self.output_value,
                                       MasterActionId=self.master_action_id)
        else:
            self.id = db.Actions.insert(Name=self.name,
                                        DeviceId=self.device_id,
                                        output_value=self.output_value,
                                        MasterActionId=self.master_action_id)
        return self.id

    @staticmethod
    def get_action_by_device(device_id):
        """
        Return list of all the actions by device
        @param device_id:
        @return:
        """
        db = current.db
        action_set = db(db.Actions.DeviceId == device_id)

        actions = []
        for action in action_set.select():
            actions.append(Action(action.id, action.name, action.DeviceId, action.outputvalue, action.masteractionid))

        return actions

    @staticmethod
    def get_action_by_user(profileid):
        """
        Return list of all the actions by user
        @param profileid:
        @return:
        """
        db = current.db
        action_set = db(db.Actions.DeviceId == db.Device.DeviceId & db.Device.ProfileId == profileid)

        actions = []
        for action in action_set.select()(db.Actions.All, groupby=db.Actions.id):
            actions.append(Action(action.id, action.name, action.DeviceId, action.outputvalue, action.masteractionid))

        return actions

    def load(self, action_id):
        """
        Loads the Action information by using the action_id provided.

        @param action_id:
        @raise:
        """
        db = current.db
        action = current.db.Action(db.Actions.id == action_id)
        if action is None:
            # TODO - define exception.
            raise

        self.id = action.id
        self.name = action.Name
        self.device_id = action.DeviceId
        self.output_value = action.OutputValue
        self.master_action_id = action.MasterActionId

    @staticmethod
    def delete(action_id):
        """
        Remove given Action from the database.

        @param action_id:
        """
        db = current.db
        action_set = db.Actions.on(MasterActionId=action_id)
        if action_set > 1 & action_set.first().id == action_id & action_id == action_set.first().MasterActionId:
            db.Actions.on(MasterActionId=action_id).update(MasterActionId=action_set[2].id)

        db(db.Actions.id == action_id).delete()

    @staticmethod
    def delete_master_and_associations(master_action_id):
        """
        Remove given Master Action and any associated action with it.

        @param master_action_id:
        """
        db = current.db
        db(db.Actions.MasterActionId == master_action_id).delete()

    @staticmethod
    def get_device_actions(device_id):
        """
        Returns list of actions associated with the current device.

        @param device_id:
        @return:
        """
        db = current.db
        actions = db(db.Actions.DeviceId == device_id)
        action_list = []
        for action in actions:
            new_action = Action(name=action.Name, device_id=action.DeviceId, output_value=action.OutputValue,
                                master_action_id=action.MasterActionId)
            new_action.id = device_id
            action_list.append(new_action)

        return action_list