from Verification import Verification

class Session:

    def __init__(self):
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

    def getUser_id(self):
        return self.userId

    def isAdministrator(self):
        return self.isAdmin
    