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
        On success returns the newly created action id.
        """
        db = current.db
        if self.id:
            db.actions(self.id).update(name=self.name,
                                       device_id=self.device_id,
                                       output_value=self.output_value,
                                       master_action_id=self.master_action_id)
        else:
            self.id = db.actions.insert(name=self.name,
                                        device_id=self.device_id,
                                        output_value=self.output_value,
                                        master_action_id=self.master_action_id)
        return self.id

    @staticmethod
    def save_action(action_id, device_id, output_value, master_action_id):
        """

        @param action_id:
        @param device_id:
        @param output_value:
        @param master_action_id:
        @return: @raise:
        """
        db = current.db

        return_val = db.actions.update_or_insert(action_id is None | db.actions.id == action_id,
                                                 device_id=device_id,
                                                 output_value=output_value,
                                                 master_action_id=master_action_id)

        if master_action_id is None:
            db(db.actions.id == return_val).update(master_action_id=return_val)
            master_action_id = return_val

        return master_action_id


    @staticmethod
    def get_action_by_device(device_id):
        """
        Return list of all the actions by device
        """
        db = current.db
        action_set = db(db.actions.device_id == device_id)

        actions = []
        for action in action_set.select():
            actions.append(
                Action(action.id, action.name, action.device_id, action.output_value, action.master_action_id))

        return actions

    @staticmethod
    def get_action_by_user(profile_id):
        """
        Return list of all the actions by user
        """
        db = current.db
        action_set = db(db.actions.device_id == db.device.device_id & db.device.profile_id == profile_id)

        actions = []
        for action in action_set.select()(db.actions.All, groupby=db.actions.id):
            actions.append(
                Action(action.id, action.name, action.device_id, action.output_value, action.master_action_id))

        return actions

    def load(self, action_id):
        """
        Loads the Action information by using the action_id provided.
        """
        db = current.db
        action = current.db.Action(db.actions.id == action_id)
        if action is None:
            # TODO - define exception.
            raise

        self.id = action.id
        self.name = action.name
        self.device_id = action.device_id
        self.output_value = action.output_value
        self.master_action_id = action.master_action_id

    @staticmethod
    def delete(action_id):
        """
        Remove given Action from the database.
        """
        db = current.db
        action_set = db.actions.on(master_action_id=action_id)
        if action_set > 1 & action_set.first().id == action_id & action_id == action_set.first().master_action_id:
            db.actions.on(master_action_id=action_id).update(master_action_id=action_set[2].id)

        db(db.actions.id == action_id).delete()

    @staticmethod
    def delete_master_and_associations(master_action_id):
        """
        Remove given Master Action and any associated action with it.
        """
        db = current.db
        db(db.actions.master_action_id == master_action_id).delete()

    @staticmethod
    def get_device_actions(device_id):
        """
        Returns list of actions associated with the current device.
        """
        db = current.db
        actions = db(db.actions.device_id == device_id)
        action_list = []
        for action in actions:
            new_action = Action(name=action.name, device_id=action.device_id, output_value=action.output_value,
                                master_action_id=action.master_action_id)
            new_action.id = device_id
            action_list.append(new_action)

        return action_list