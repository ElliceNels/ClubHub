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
        self.isCoord = Verification.isCoord(self.userId)
        self.isAdmin = Verification.isAdmin(self.userId)

    def logout(self):
        self.userId = None
        self.isLoggedIn = False

    def isCoordinator(self):
        return self.isCoord
        

    def isAdministrator(self):
        return self.isAdmin
    