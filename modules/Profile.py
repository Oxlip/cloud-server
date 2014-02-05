""" Class to handle USER Profiles
"""
from gluon import current
from modules.PlugZExceptions import *


class Profile:
    def __init__(self, profile_id=None, username=None, first_name=None, last_name=None, date_of_birth=None, gender=None,
                 email=None, contact_info_list=[]):
        """
        Get user details based on the profile ID,  This method will return User object.
        """
        self.profile_id = profile_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.date_of_birth = date_of_birth
        self.gender = gender
        self.email = email
        self.contact_info_list = contact_info_list

    @staticmethod
    def register_profile(username, first_name, last_name, date_of_birth, gender, email, contact_info):
        """
        Register a new User in to the system.
        This information would come from Google, Yahoo or Facebook  as part of New user registration
        """
        db = current.db

        if Profile.get_user(username):
            raise AlreadyExistsError('Username already in use.')

        if Profile.is_email_registered(email):
            raise AlreadyExistsError('Email is already registered')

        profile_id = db.profile.insert(username=username,
                                       first_name=first_name,
                                       last_name=last_name,
                                       date_of_birth=date_of_birth,
                                       gender=gender,
                                       email=email)

        db.UserContactInfo.insert(profile_id=profile_id,
                                  address_line_1=contact_info.address_line_1,
                                  address_line_2=contact_info.address_line_2,
                                  city_id=contact_info.city.id,
                                  postal_code=contact_info.postal_code,
                                  email=contact_info.email,
                                  phone=contact_info.phone)

        return Profile.get_user(username)

    @staticmethod
    def login(email):
        """
        Every time a new user Login's to application this Method is called.
        """
        db = current.db

        if not Profile.is_email_registered(email):
            raise NotFoundError('User does not Exists {0}'.format(email))

        profile_id = db(db.user_contact_info.email == email).select(db.user_contact_info.profile_id).first()
        profile = Profile()
        profile.load(profile_id)
        return profile

    def _load(self, profile):
        """
        Internal method to fill self with DAL profile object
        """
        self.__init__(profile_id=profile.id, username=profile.username, first_name=profile.first_name,
                      last_name=profile.last_name, date_of_birth=profile.date_of_birth, gender = profile.gender,
                      email=profile.email)

    def load(self, profile_id):
        """
         Returns user for the given Profile ID
        """
        db = current.db
        profile = db(db.profile.id == profile_id).select().first()
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

        #If the contact info is alreay loaded then use it.
        if len(self.contact_info_list) > 0:
            return self.contact_info_list

        contact_infos = db(db.user_contact_info.profile_id == self.profile_id).select()
        for contact_info in contact_infos:
            c = UserContactInfo()
            c.load(contact_info.id)
            self.contact_info_list.append(c.__dict__)

        return self.contact_info_list

    @staticmethod
    def is_email_registered(email):
        """
        Check if the email is already registered.  This function will be called by Login and Register Profile function
        """
        db = current.db
        return not db(db.user_contact_info.email == email).isempty()

class UserContactInfo:
    def __init__(self, id=None, profile_id=None, contact_type=None,
                 address_line_1=None, address_line_2=None, city=None, postal_code=None, phone=None):
        self.id = id
        self.profile_id = profile_id
        self.contact_type = contact_type
        self.address_line_1 = address_line_1
        self.address_line_2 = address_line_2
        self.city = city
        self.postal_code = postal_code
        self.phone = phone

    def load(self, id):
        db = current.db
        contact_info = db(db.user_contact_info.id == id).select().first()
        if contact_info is None:
            raise NotFoundError('UserContactInfo not found {0}'.format(id))
        city = City(contact_info.city_id).__dict__
        self.__init__(id=id, profile_id=contact_info.profile_id, contact_type=contact_info.contact_type,
                      address_line_1=contact_info.address_line_1, address_line_2=contact_info.address_line_2,
                      postal_code=contact_info.postal_code, phone=contact_info.phone, city=city)


class City:
    def __init__(self, id):
        db = current.db
        record = db((db.city.id == id) & (db.states.id == db.city.state_id) & (db.country.id == db.states.country_id)).select().first()
        if record is None:
            raise NotFoundError('City not found {0}'.format(id))
        self.id = id
        self.city = record.city.name
        self.state = record.states.name
        self.country = record.country.name


