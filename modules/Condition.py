""" Class to Manage and create Conditions
"""

import sys

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
        for condition in db(
                                db.rules.profile_id == profile_id & db.conditions.master_condition_id == db.rules.condition_id):
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
    def save_condition(device_id, compares, condition_value, is_and_operation, master_condition_id):

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
            return_val = db.conditions.update_or_insert(device_id=device_id,
                                                        compares=compares,
                                                        condition_value=condition_value,
                                                        is_and_operation=is_and_operation,
                                                        master_condition_id=master_condition_id)

            if master_condition_id is None:
                db(db.conditions.id == return_val).update(master_condition_id=return_val)
                master_condition_id = return_val

            return master_condition_id
        except:
            # TODO: Log Exception
            exception = sys.exc_info()[0]
            raise exception


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


    @staticmethod
    def add_rule(ruleid, profileid, rulename, conditionid, actionid):

        """
        @param ruleid:
        @param profileid:
        @param rulename:
        @param conditionid:
        @param actionid:
        @return:
        """

        try:
            db = current.db
            rule_id = db.rules.update_or_insert(profile_id=profileid,
                                                name=rulename,
                                                condition_id=conditionid,
                                                action_id=actionid,
                                                is_active=True)
            db.commit()
            return rule_id
        except:
            # TODO: Log Exception
            exception = sys.exc_info()[0]
            raise exception


    @staticmethod
    def get_all_rules(profile_id):
        try:
            db = current.db
            complete_rule = db(
                (db.rules.profile_id == profile_id) & (db.rules.is_active == True) & (
                    db.rules.condition_id == db.conditions.master_condition_id) &
                (db.rules.action_id == db.actions.id) & (db.actions.id == db.action_details.action_id))

            return complete_rule

        except:  # TODO: Log Exception
            exception = sys.exc_info()[0]
            raise exception


@staticmethod
def publish_rule_to_hub(profile_id, rule_id, rule_expression):
    import PushNotification

    PushNotification.notify_rule_change(profile_id)