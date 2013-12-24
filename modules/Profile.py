from gluon import current

""" Class to handle USER Profiles
"""
class Profile:

    """ Get user details based on the profile ID,  This method will return User object.
    """
    def __init__(self, profileId):
        self.ProfileId = profileId
        self.UserName = None
        self.FirstName = None
        self.LastName = None
        self.DateOfBirth = None
        self.Gender = None
        self.AddressLine1 = None
        self.AddressLine2 = None
        self.City = None
        self.CityId = None
        self.State = None
        self.StateId = None
        self.Country = None
        self.Zip = None
        self.Email = None
        self.Phone = None


    """ Register a new User in to the system.  This information would come from Google, Yahoo or Facebook  as part of New user registration
    """
    @staticmethod
    def RegisterProfile(self, EmailId, UserName, FirstName, LastName, DateOfBirth, IsMale, AddressLine1=None, AddressLine2=None, City=None, State=None, Country=None, Zip=None, phone=None ):

        db = current.db

        if IsUserExist(EmailId):
            raise 'User Exists'  #TODO: Define Exception

        self.ProfileId =  db.Profile.insert(UserName = username,
                                     FirstName = FirstName,
                                     LastName = LastName,
                                     DateOfBirth = DateOfBirth,
                                     Gender = isMale,
                                     MasterProfileId = self.id if self.id else MasterProfileId)
        return GetUser()


    """ Everytime a new user Login's to application this Method is called.
    """
    @staticmethod
    def Login(self, emailId):

        db = current.db

        if not IsUserExist(EmailId):
            raise 'User does not Exists' #TODO: Define Exception

        self.ProfileId = db(db.UserContactInfo.Email == emailId).select(ProfileId).first();
        return GetUser()

    """ Returns user for the given Profile ID
    """
    def GetUser(self):
        user  = db(db.Profile.id==self.id &
                    db.Profile.id == db.UserContactInfo.ProfileId &
                    db.UserContactInfo.City == db.City.id &
                    db.UserContactInfo.StateId == db.States.id &
                    db.States.Country == db.Country.id).select()
        #TODO: Move Contact Info to seperate Clas
        self.UserName = user.UserName
        self.FirstName = user.FirstName
        self.LastName = user.LastName
        self.DateOfBirth = user.DateOfBirth
        self.Gender = "Male" if user.Gender == 1 else "Female"
        self.AddressLine1 = user.AddressLine1
        self.AddressLine2 = user.AddressLine2
        self.City = user.City.Name
        self.CityId = user.City.id
        self.State = user.States.Name
        self.StateId = user.States.id
        self.Country = user.Country.Name
        self.Zip = user.Zip
        self.Phone = user.Phone

    """ Check if use Exists.  This function will be called by Login and Register Profile function
    """
    @staticmethod
    def IsUserExist(self, emailId):
        db = current.db
        return not db(db.UserContactInfo.Email == emailId).isempty()

    """ Function to un-enroll user from the program.
    REVISION NEED - Complete Rewrite

    @staticmethod
    def DeactivateProfile(self, EmailId):
        db = current.db
        if not IsUserExist(EmailId):
            raise 'User does not Exists'
        else:
            try:
                db(db.Profile.id == ProfileId).update(IsActive = False)
                return True
            except:
                #Log Here [ERROR]  on Exception
                return False

    """