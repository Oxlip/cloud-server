""" Class to handle USER Profiles
"""
from gluon import current
from modules.PlugZExceptions import *

class Profile:
    def __init__(self, profile_id=None, username=None, first_name=None, last_name=None, date_of_birth=None, gender=None,
                 master_profile_id=None, contact_info_list=[]):
        """
        Get user details based on the profile ID,  This method will return User object.
        """
        self.profile_id = profile_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.contact_info_list = contact_info_list

    @staticmethod
    def register_profile(self, email, username, first_name, last_name, date_of_birth, gender,
                         master_profile_id=None, contact_info=None):
        """
        Register a new User in to the system.
        This information would come from Google, Yahoo or Facebook  as part of New user registration
        """
        db = current.db

        if self.is_user_exist(username):
            raise AlreadyExistsError('Username already in use.')

        if self.is_email_registered(email):
            raise AlreadyExistsError('Email is already registered')

        profile_id = db.profile.insert(username=username,
                                       first_name=first_name,
                                       last_name=last_name,
                                       date_of_birth=date_of_birth,
                                       gender=gender,
                                       master_profile_id=None)

        db(db.profile.id == id).update(
            master_profile_id=master_profile_id if master_profile_id is not None else profile_id)

        db.UserContactInfo.insert(profile_id=profile_id,
                                  address_line_1=contact_info.address_line_1,
                                  address_line_2=contact_info.address_line_2,
                                  state_id=1, #Remove this we dont want state_id in contactinfo
                                  city_id=contact_info.city.id,
                                  postalcode=contact_info.postal_code,
                                  email=contact_info.email,
                                  phone=contact_info.phone)

        return self.get_user()

    @staticmethod
    def login(self, email):
        """
        Every time a new user Login's to application this Method is called.
        """
        db = current.db

        if not self.is_user_exist(email):
            raise NotFoundError('User does not Exists {0}'.format(email))

        self.profile_id = db(db.user_contact_info.email == email).select(db.user_contact_info.profile_id).first();
        return self.get_user()

    def _load(self, profile):
        """
        Internal method to fill self with DAL profile object
        """
        self.username = profile.username
        self.first_name = profile.first_name
        self.last_name = profile.last_name
        self.date_of_birth = profile.date_of_birth
        self.gender = profile.gender

    def load(self):
        """
         Returns user for the given Profile ID
        """
        db = current.db
        profile = db(db.profile.id == self.profile_id).select().first()
        self._load(profile)

    @staticmethod
    def get_user(username):
        """
         Returns user for the given usernam
        """
        db = current.db
        profile = db(db.profile.username == username).select().first()
        user = Profile()
        user._load(profile)
        return user

    def get_user_contact_info(self):
        """
        Returns contact infos of a user as a list
        """
        db = current.db
        if self.contact_info_list is not None and len(self.contact_info_list) != 0:
            return self.contact_info_list

        for contact_info in db(db.user_contact_info.profile_id == self.profile_id).select():
            c = UserContactInfo()
            self.contact_info_list.append(c.load(contact_info.id))

        return self.contact_info_list

    @staticmethod
    def is_email_registered(email):
        """
        Check if the email is already registered.  This function will be called by Login and Register Profile function
        """
        db = current.db
        return not db(db.user_contact_info.email == email).isempty()

    def deactivate_profile(self, profile_id):
        """
        Function to un-enroll user from the program.
        """
        db = current.db
        if not self.is_user_exist(db.user_contact_info.on(profile_id == db.user_contact_info.profile_id).select(
                db.user_contact_info.email).First()):
            raise 'User does not exists'        # TODO: Handle Exception

        profile_set = db.profile.on(master_profile_id=profile_id)
        if profile_set > 1 & profile_set.id == profile_id & profile_set == profile_set.master_profile_id:
            db.profile.on(master_profile_id=profile_id).update(master_profile_id=profile_set[2].id)

        db(db.profile.id == profile_id).update(db.profile.isActive == False)


class UserContactInfo:
    def __init__(self, id=None, profile_id=None,
                 address_line_1=None, address_line_2=None, city=None, postal_code=None,
                 email=None, phone=None):
        self.id = id
        self.profile_id = profile_id
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.postal_code = postal_code
        self.email = email
        self.phone = phone

    def load(self, id):
        db = current.db
        contact_info = db(db.user_contact_info.id == id).select()
        if contact_info is None:
            raise NotFoundError('UserContactInfo not found {0}'.format(id))
        self.id = id
        self.profile_id = contact_info.profile_id
        self.address_line_1 = contact_info.address_line_1
        self.address_line_2 = contact_info.address_line_2
        self.postal_code = contact_info.postal_code
        self.email = contact_info.email
        self.phone = contact_info.phone
        self.city = City(contact_info.city_id)


class City:
    def __init__(self, id):
        db = current.db
        city = db(db.city.id == id & db.states.id == db.city.state & db.country.id == db.states.country).select()
        if city is None:
            raise NotFoundError('City not found {0}'.format(id))
        self.id = id
        self.city = city.name
        self.state = city.state.name
        self.country = city.country.name


