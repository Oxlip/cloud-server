""" Class to handle USER Profiles
"""
from gluon import current


class Profile:
    def __init__(self, profile_id):
        """
        Get user details based on the profile ID,  This method will return User object.
        @param profile_id:
        """
        self.profile_id = profile_id
        self.username = None
        self.first_name = None
        self.last_name = None
        self.date_of_birth = None
        self.gender = None
        self.address_line_1 = None
        self.address_line_2 = None
        self.city = None
        self.city_id = None
        self.state = None
        self.state_id = None
        self.country = None
        self.postal_code = None
        self.email = None
        self.phone = None

    @staticmethod
    def register_profile(self, email, username, first_name, last_name, date_of_birth, is_male,
                         address_line_1=None, address_line_2=None, city=None, state=None, postal_code=None, phone=None,
                         master_profile_id=None):

        """
        Register a new User in to the system.
        This information would come from Google, Yahoo or Facebook  as part of New user registration
        @param self:
        @param email:
        @param username:
        @param first_name:
        @param last_name:
        @param date_of_birth:
        @param is_male:
        @param address_line_1:
        @param address_line_2:
        @param city:
        @param state:
        @param country:
        @param zip:
        @param phone:
        @return: @raise 'User Exists':
        """
        db = current.db

        if self.is_user_exist(email):
            raise 'User Exists'  #TODO:Define Exception

        profile_id = db.profile.insert(username=username,
                                       first_name=first_name,
                                       last_name=last_name,
                                       date_of_birth=date_of_birth,
                                       gender=is_male,
                                       master_profile_id=None)

        db(db.profile.id == id).update(
            master_profile_id=master_profile_id if master_profile_id is not None else profile_id)

        db.UserContactInfo.insert(profile_id=profile_id,
                                  address_line_1=address_line_1,
                                  address_line_2=address_line_2,
                                  state_id=state, #TODO: Need to handle State from FB, Google, Twitter
                                  city_id=city, #TODO: Need to handle City from FB, Google, Twitter
                                  postalcode=postal_code,
                                  email=email,
                                  phone=phone)

        return self.get_user()

    @staticmethod
    def login(self, email):

        """
        Every time a new user Login's to application this Method is called.
        @param self:
        @param email:
        @return: @raise 'User does not Exists':
        """
        db = current.db

        if not self.is_user_exist(email):
            raise 'User does not Exists' #TODO: Define Exception

        self.profile_id = db(db.user_contact_info.email == email).select(db.user_contact_info.profile_id).first();
        return self.get_user()

    def get_user(self):
        """
         Returns user for the given Profile ID
        """
        db = current.db

        user = db(db.profile.id == self.profile_id & db.profile.id == db.user_contact_info.profile_id &
                  db.user_contact_info.city_id == db.city.id & db.user_contact_info.StateId == db.states.id &
                  db.states.country == db.country.id).select().first()

        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.date_of_birth = user.date_of_birth
        self.gender = "Male" if user.gender == 1 else "Female"
        self.address_line_1 = user.address_line_1
        self.address_line_2 = user.address_line_2
        self.city = user.city.name
        self.city_id = user.city.id
        self.state = user.states.Name
        self.state_id = user.states.id
        self.country = user.country.Name
        self.postal_code = user.postalcode
        self.phone = user.phone
        self.email = user.email

    @staticmethod
    def is_user_exist(email):
        """
        Check if use Exists.  This function will be called by Login and Register Profile function
        @param email:
        @return:
        """
        db = current.db
        return not db(db.user_contact_info.email == email).isempty()

    def deactivate_profile(self, profile_id):
        """
        Function to un-enroll user from the program.
        @rtype : object
        @param profile_id:
        @raise 'User does not exists':
        """
        db = current.db
        if not self.is_user_exist(db.user_contact_info.on(profile_id == db.user_contact_info.profile_id).select(
                db.user_contact_info.email).First()):
            raise 'User does not exists'        # TODO: Handle Exception

        profile_set = db.profile.on(master_profile_id=profile_id)
        if profile_set > 1 & profile_set.id == profile_id & profile_set == profile_set.master_profile_id:
            db.profile.on(master_profile_id=profile_id).update(master_profile_id=profile_set[2].id)

        db(db.profile.id == profile_id).update(db.profile.isActive == False)
