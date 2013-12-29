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

        profile_id = db.Profile.insert(UserName=username,
                                       FirstName=first_name,
                                       LastName=last_name,
                                       DateOfBirth=date_of_birth,
                                       Gender=is_male,
                                       MasterProfileId=None)

        db(db.Profile.id == id).update(
            MasterProfileId=master_profile_id if master_profile_id is not None else profile_id)

        db.UserContactInfo.insert(ProfileId=profile_id,
                                  AddressLine1=address_line_1,
                                  AddressLine2=address_line_2,
                                  StateId=state, #TODO: Need to handle State from FB, Google, Twitter
                                  City=city, #TODO: Need to handle City from FB, Google, Twitter
                                  Zip=postal_code,
                                  Email=email,
                                  Phone=phone)

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

        self.profile_id = db(db.UserContactInfo.Email == email).select(db.UserContactInfo.ProfileId).first();
        return self.get_user()

    def get_user(self):
        """
         Returns user for the given Profile ID
        """
        db = current.db

        user = db(db.Profile.id == self.profile_id & db.Profile.id == db.UserContactInfo.ProfileId &
                  db.UserContactInfo.City == db.City.id & db.UserContactInfo.StateId == db.States.id &
                  db.States.Country == db.Country.id).select().first()

        self.username = user.UserName
        self.first_name = user.FirstName
        self.last_name = user.LastName
        self.date_of_birth = user.DateOfBirth
        self.gender = "Male" if user.Gender == 1 else "Female"
        self.address_line_1 = user.AddressLine1
        self.address_line_2 = user.AddressLine2
        self.city = user.City.Name
        self.city_id = user.City.id
        self.state = user.States.Name
        self.state_id = user.States.id
        self.country = user.Country.Name
        self.postal_code = user.Zip
        self.phone = user.Phone

    @staticmethod
    def is_user_exist(email):
        """
        Check if use Exists.  This function will be called by Login and Register Profile function
        @param email:
        @return:
        """
        db = current.db
        return not db(db.UserContactInfo.Email == email).isempty()

    def deactivate_profile(self, profile_id):
        """
        Function to un-enroll user from the program.
        @rtype : object
        @param profile_id:
        @raise 'User does not exists':
        """
        db = current.db
        if not self.is_user_exist(db.UserContactInfo.on(profile_id == db.UserContactInfo.ProfileId).select(
                db.UserContactInfo.Email).First()):
            raise 'User does not exists' #TODO: Handle Exception

        profile_set = db.Profile.on(MasterProfileId=profile_id)
        if profile_set > 1 & profile_set.id == profile_id & profile_set == profile_set.MasterProfileId:
            db.Profile.on(MasterProfileId=profile_id).update(MasterProfileId=profile_set[2].id)

        db(db.Profile.id == profile_id).update(db.Profile.isActive == False)