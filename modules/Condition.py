""" Class to Manage and create Conditions
"""

from gluon import current


class Condition:
    def __init__(self):
        self.condition_id = None
        self.device_id = None
        self.operator = None
        self.condition_value = None
        self.is_and_operator = None
        self.master_condition_id = None

    @staticmethod
    def get_conditions(master_condition_id):
        """
        Get conditions based on condition_id
        @param master_condition_id:
        @return:
        """
        db = current.db

        conditionlist = []
        for condition in db(db.Conditions.MasterCondtionId == master_condition_id):
            _condition = Condition()
            _condition.condition_id = condition.id
            _condition.device_id = condition.DeviceId
            _condition.operator = condition.Operator
            _condition.condition_value = condition.ConditionValue
            _condition.is_and_operator = condition.isAndOpertor
            _condition.master_condition_id = condition.MasterCondtionId
            conditionlist.append(_condition)

        return conditionlist

    @staticmethod
    def get_conditions_by_user(profile_id):

        """
        Get All conditions defined by user
        @param profile_id:
        @return:
        """
        db = current.db

        conditionlist = []
        for condition in db(db.Rules.ProfileId == profile_id & db.Condtions.MasterCondtionId == db.Rules.ConditionId):
            _condition = Condition()
            _condition.condition_id = condition.id
            _condition.device_id = condition.DeviceId
            _condition.operator = condition.Operator
            _condition.condition_value = condition.ConditionValue
            _condition.is_and_operator = condition.isAndOpertor
            _condition.master_condition_id = condition.MasterCondtionId
            conditionlist.append(_condition)

        return conditionlist

    @staticmethod
    def save_condition(condition_id, device_id, operator, condition_value, is_and_operator, master_condition_id):

        """
        Insert/Update an existing condition
        @param condition_id:
        @param device_id:
        @param operator:
        @param condition_value:
        @param is_and_operator:
        @param master_condition_id:
        @return: @raise:
        """
        db = current.db

        try:
            return db.Conditions.update_or_insert(condition_id is None | db.Conditions.ConditionId == condition_id,
                                                  DeviceId=device_id,
                                                  Operatr=operator,
                                                  ConditionValue=condition_value,
                                                  IsAndOperation=is_and_operator,
                                                  MasterConditionId=master_condition_id)
        except:
            # TODO: Log Exception
            raise

    @staticmethod
    def remove_condition(condition_id):
        """
        Remove a condition from the Database
        @param condition_id:
        """
        db = current.db
        condition_set = db.Conditions.on(MasterConditionid=condition_id)
        if condition_set > 1 & condition_set.id == condition_id & condition_id == condition_set.MasterConditionId:
            db.Conditions.on(db.Conditions.MasterCondtionId == condition_id).update(
                MasterConditionid=condition_set[2].id)

        db(db.Conditions.id == condition_id).delete()