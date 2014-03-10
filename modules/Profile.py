""" Class to handle USER Profiles
"""
from gluon import current
from datetime import datetime
import PlugZExceptions
import PushNotification


class Profile:
    def __init__(self, profile_id=None, username=None, first_name=None, last_name=None, email=None, photo=None,
                 identifier=None, contact_info_list=[]):
        """
        Get user details based on the profile ID,  This method will return User object.
        """
        self.profile_id = profile_id
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.photo = photo
        self.identifier = identifier
        self.contact_info_list = contact_info_list

    @staticmethod
    def register_profile(username, first_name, last_name, email, photo, identifier, contact_info=None):
        """
        Register a new user in to the system.
        This information would come from janrain(Google, Yahoo or Facebook) as part of new user registration
        """
        db = current.db

        try:
            if Profile.get_user(username):
                raise PlugZExceptions.AlreadyExistsError('Username already in use.')
        except PlugZExceptions.NotFoundError:
            pass

        if Profile.is_email_registered(email):
            raise PlugZExceptions.AlreadyExistsError('Email is already registered')

        profile_id = db.profile.insert(username=username,
                                       first_name=first_name,
                                       last_name=last_name,
                                       email=email,
                                       photo=photo,
                                       identifier=identifier)
        if contact_info:
            db.UserContactInfo.insert(profile_id=profile_id,
                                      address_line_1=contact_info.address_line_1,
                                      address_line_2=contact_info.address_line_2,
                                      city_id=contact_info.city.id,
                                      postal_code=contact_info.postal_code,
                                      phone=contact_info.phone)
        db.commit()

        return Profile.get_user(username)

    def get_status_channel(self):
        """
        Returns channel id to communicate with the mobile/browser(for status updates).
        """
        #TODO - Change the channel name to random one for security reasons
        return 'status_channel_' + self.username

    @staticmethod
    def login(email):
        """
        Every time a new user Login's to application this Method is called.
        """
        db = current.db

        if not Profile.is_email_registered(email):
            raise PlugZExceptions.NotFoundError('User does not Exists {0}'.format(email))

        # Load the profile
        profile = Profile()
        profile._load(db(db.profile.email == email).select().first())

        #Logout previous session
        Profile.logout(profile.profile_id)

        # Insert an entry to User sessions
        user_session = db.user_session.insert(profile_id=profile.profile_id, connect_time=datetime.utcnow(),
                                              channel=profile.get_status_channel())

        return profile.username, user_session.id, profile.profile_id

    @staticmethod
    def logout(user_session_id):
        """
        Disconnects a user session
        """
        db = current.db
        sessions = db(db.user_session.id == user_session_id).select()
        for session in sessions:
            session.disconnect_time = datetime.utcnow()
            session.update_record()

    def _load(self, profile):
        """
        Internal method to fill self with DAL profile object
        """
        self.__init__(profile_id=profile.id, username=profile.username, first_name=profile.first_name,
                      last_name=profile.last_name, email=profile.email, photo=profile.photo,
                      identifier=profile.identifier)

    @staticmethod
    def load(profile_id):
        """
         Returns user for the given Profile ID
        """
        db = current.db
        profile = db(db.profile.id == profile_id).select().first()
        if profile is None:
            raise PlugZExceptions.NotFoundError('user not found {0}'.format(username))
        p = Profile()
        p._load(profile)
        return p

    @staticmethod
    def get_user(username):
        """
         Returns user for the given usernam
        """
        db = current.db
        profile = db(db.profile.username == username).select().first()
        if profile is None:
            raise PlugZExceptions.NotFoundError('user not found {0}'.format(username))
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
        return not db(db.profile.email == email).isempty()

    def record_device_value_changed(self, device_id, value):
        """
        Records an activity done by the user - a device's value changed.
        """
        db = current.db
        db.user_activity.insert(profile_id=self.profile_id, activity_date=datetime.utcnow(),
                                device_id=device_id, output_value=value)
        db.commit()

        # Command Hub to do this work
        PushNotification.set_device_status(device_id, value)

        # TODO - Send status update to the clients

    def record_action_executed(self, action_id):
        """
        Records an activity done by the user - action executed.
        """
        db = current.db
        db.user_activity.insert(profile_id=self.profile_id, activity_date=datetime.utcnow(), action_id=device_id)
        db.commit()

        # Command Hub to do this work
        PushNotification.execute_action(action_id)

        # TODO - Send status update to the clients


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
            raise PlugZExceptions.NotFoundError('UserContactInfo not found {0}'.format(id))
        city = City(contact_info.city_id).__dict__
        self.__init__(id=id, profile_id=contact_info.profile_id, contact_type=contact_info.contact_type,
                      address_line_1=contact_info.address_line_1, address_line_2=contact_info.address_line_2,
                      postal_code=contact_info.postal_code, phone=contact_info.phone, city=city)


class City:
    def __init__(self, id):
        db = current.db
        record = db((db.city.id == id) & (db.states.id == db.city.state_id) & (db.country.id == db.states.country_id)).select().first()
        if record is None:
            raise PlugZExceptions.NotFoundError('City not found {0}'.format(id))
        self.id = id
        self.city = record.city.name
        self.state = record.states.name
        self.country = record.country.name


