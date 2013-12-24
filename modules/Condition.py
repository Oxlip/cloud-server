from gluon import current
db = current.db

""" Class to Manage and create Conditions
"""

class Condition:
    def __init__(self):
        self.CondtionId = None
        self.DeviceId = None
        self.Operator = None
        self.ConditionValue = None
        self.isAndOpertor = None
        self.MasterCondtionId = None

    """Get conditions based on ConditionId
    """
    def GetConditions(self, MasterConditionId):
        conditionList = []
        for condition in db(db.Conditions.MasterCondtionId == MasterConditionId):
            _condition = Condition()
            _condition.CondtionId = condition.id
            _condition.DeviceId = condition.DeviceId
            _condition.Operator = condition.Operator
            _condition.ConditionValue = condition.ConditionValue
            _condition.isAndOpertor = condition.isAndOpertor
            _condition.MasterCondtionId = condition.MasterCondtionId
            conditionList.append(_condition)

        return conditionList


    """Get All conditions defined by user
    """
    def GetConditionsByUser(self, ProfileId):
        conditionList = []
        for condition in db(db.Rules.ProfileId == ProfileId & db.Condtions.MasterCondtionId == db.Rules.ConditionId):
            _condition = Condition()
            _condition.CondtionId = condition.id
            _condition.DeviceId = condition.DeviceId
            _condition.Operator = condition.Operator
            _condition.ConditionValue = condition.ConditionValue
            _condition.isAndOpertor = condition.isAndOpertor
            _condition.MasterCondtionId = condition.MasterCondtionId
            conditionList.append(_condition)

        return conditionList



    """ Insert/Update an existing condition
    """
    def SaveCondition(self, ConditionId, DeviceId, Operator, ConditionValue, IsAndOperator, MasterConditionId):
        try:

            return db.Conditions.update_or_insert(ConditionId == None | db.Conditions.ConditionId == ConditionId,
                                                  DeviceId = DeviceId,
                                                  Operatr = Operator,
                                                  ConditionValue = ConditionValue,
                                                  IsAndOperation = IsAndOperator,
                                                  MasterConditionId = MasterConditionId)

        except:
            # TODO: Log Exception
            raise

    """ Remove a condition from the Database

    def RemoveCondition(self, ConditionId):
        conditionSet = db.Conditions.on(MasterConditionid = ConditionId)
        if conditionSet.count > 1 && conditionSet.select().first().id == ConditionId:





        raise

    """
