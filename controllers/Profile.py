class Profile:
    
    def RegisterProfile(self,  EmailId, username=None, FirstName=None, LastName=None, DateOfBirth=None, isMale=None, AddressLine1=None, AddressLine2=None, City=None, State=None, Country=None, Zip=None, phone=None ):
        raise
    
    def Login(self, emailId):        
        raise
    
    def IsUserExist(self, emailId):
        return True
    
    def GetUser(self, profileId):
        raise
    
    def DeactivateProfile(self, emailId):
        raise
