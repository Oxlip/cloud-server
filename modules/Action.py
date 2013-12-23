from gluon import current

""" Simply put an action associates a value with an device.
    It also links multiple actions into one(through MasterAction).
"""
class Action:
    def __init__(self, Name=None, DeviceId=None, OutputValue=None, MasterActionId=None):
        self.Id = None
        self.Name = Name
        self.DeviceId = DeviceId
        self.OutputValue = OutputValue
        self.MasterActionId = MasterActionId

    """ Saves the current DeviceData.
    
        On success returns the newly created deviceId.
    """
    def Save(self):
        db = current.db
        if (self.Id):
            db.Actions(self.Id).update(Name = self.Name,
                                       DeviceId = self.DeviceId,
                                       OutputValue = self.OutputValue,
                                       MasterActionId = self.MasterActionId
                                       )
        else:
            self.Id = db.Actions.insert(Name = self.Name,
                                        DeviceId = self.DeviceId,
                                        OutputValue = self.OutputValue,
                                        MasterActionId = self.MasterActionId
                                        )
        return self.Id

    """ Loads the Action information by using the ActionId provided.
    """
    def Load(self, ActionId):
        action = current.db.Action(ActionId)
        if action == None:
            # TODO - define exception.
            raise
        
        self.Id = action.id
        self.Name = action.Name
        self.DeviceId = action.DeviceId
        self.OutputValue = action.OutputValue
        self.MasterActionId = action.MasterActionId
    
    """ Remove given Action from the database.
    """
    def Delete(self):
        db = current.db
        # special case - deleting the master action. 
        if db.Actions.id == db.MasterActionId:
            actions = db(db.Actions.MasterActionId == ActionId)
            # We need worry only if there atleast 1 slave.
            if actions.count() > 1:
                # Upgrade the 2nd action as master action.
                newMasterActionId = actions[2].id
                db(db.Actions.MasterActionId == ActionId).update(MasterActionId = newMasterActionId)

        # delete the master action
        db(db.Actions.id == ActionId).delete()

    """ Remove given Master Action and any associated action with it.
    """
    @staticmethod
    def DeleteMasterAndAllActions(MasterActionId):
        current.db(db.Actions.MasterActionId == MasterActionId).delete()
    
    """ Returns list of actions associated with the current device. 
    """
    def GetDeviceActions(self, DeviceId):
        actions = current.db(db.Actions.DeviceId == DeviceId)
        action_list = []
        for action in actions:
            new_action = Action(Name=action.Name, DeviceId=action.DeviceId, OutputValue=action.OutputValue, MasterActionId=action.MasterActionId)
            new_action.Id = DeviceId
            action_list.append(new_action)
            
        return action_list
    
    