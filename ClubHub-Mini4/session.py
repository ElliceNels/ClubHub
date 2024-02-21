from Verification import Verification

class Session:

    def __init__(self):
        self.user_id = None
        self.is_coord = False
        self.is_admin = False
        self.is_logged_in = False

    def login(self, user_id):
        self.user_id = user_id
        self.is_logged_in = True
        self.is_coord = Verification.isCoord(self.user_id)
        self.is_admin = Verification.isAdmin(self.user_id)

    def logout(self):
        self.user_id = None
        self.is_logged_in = False

    def isCoordinator(self):
        return self.is_coord

    def getUser_id(self):
        return self.user_id

    def isAdministrator(self):
        return self.is_admin
    