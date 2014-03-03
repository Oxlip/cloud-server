""" Class to Manage and create Conditions
"""

from gluon import current


class Condition:
    def __init__(self):
        self.condition_id = None
        self.device_id = None
        self.compares = None
        self.condition_value = None
        self.is_and_operation = None
        self.master_condition_id = None

    @staticmethod
    def get_conditions(master_condition_id):
        """
        Get conditions based on condition_id
        @param master_condition_id:
        @return:
        """
        db = current.db

        condition_list = []
        for condition in db(db.conditions.master_condition_id == master_condition_id):
            _condition = Condition()
            _condition.condition_id = condition.id
            _condition.device_id = condition.device_id
            _condition.compares = condition.compares
            _condition.condition_value = condition.condition_value
            _condition.is_and_operation = condition.is_and_operation
            _condition.master_condition_id = condition.master_condition_id
            condition_list.append(_condition)

        return condition_list

    @staticmethod
    def get_conditions_by_user(profile_id):

        """
        Get All conditions defined by user
        @param profile_id:
        @return:
        """
        db = current.db

        condition_list = []
        for condition in db(db.rules.profile_id == profile_id & db.conditions.master_condition_id == db.rules.condition_id):
            _condition = Condition()
            _condition.condition_id = condition.id
            _condition.device_id = condition.device_id
            _condition.compares = condition.compares
            _condition.condition_value = condition.condition_value
            _condition.is_and_operation = condition.is_and_operation
            _condition.master_condition_id = condition.master_condition_id
            condition_list.append(_condition)

        return condition_list

    @staticmethod
    def save_condition(condition_id, device_id, compares, condition_value, is_and_operation, master_condition_id):

        """
        Insert/Update an existing condition
        @param condition_id:
        @param device_id:
        @param compares:
        @param condition_value:
        @param is_and_operation:
        @param master_condition_id:
        @return: @raise:
        """
        db = current.db

        try:
            return db.conditions.update_or_insert(condition_id is None | db.conditions.id == condition_id,
                                                  device_id=device_id,
                                                  compares=compares,
                                                  condition_value=condition_value,
                                                  is_and_operation=is_and_operation,
                                                  master_condition_id=master_condition_id)
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
        condition_set = db.conditions.on(master_condition_id=condition_id)
        if condition_set > 1 & condition_set.id == condition_id & condition_id == condition_set.master_condition_id:
            db.conditions.on(db.conditions.master_condition_id == condition_id).update(
                master_condition_id=condition_set[2].id)

        db(db.conditions.id == condition_id).delete()