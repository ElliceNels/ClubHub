from Verification import Verification

class Session:

    def __innit__(self):
        self.userId = None
        self.isCoord = False
        self.isAdmin = False
        self.isLoggedIn = False

    def login(self, userId):
        self.userId = userId
        self.isLoggedIn = True

    def logout(self):
        self.userId = None
        self.isLoggedIn = False

    def isCoordinator(self):
        self.isCoord = Verification.isCoord(self.userId)
        return self.isCoord
        

    def isAdministrator(self):
        self.isAdmin = Verification.isAdmin(self.userId)
        return self.isAdmin
    