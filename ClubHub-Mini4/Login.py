import re

class Login:
    def __init__(self):
        self.alert = []

    def signupValidation(self, firstname, lastname, userId, email, username, password1, password2, usertype):
        self.nameValidator(firstname, lastname)
        self.accountTypeValidator(userId, usertype)
        self.usernameValidator(username)
        self.passwordValidator(password1, password2)
        self.emailValidator(email)
        return self.alert

    def nameValidator(self, firstname, lastname):
        firstname = firstname.strip()
        lastname = lastname.strip()
        if len(firstname) <= 2 or len(lastname) <= 2:
            self.alert.append("First name and last name must both be at least 2 characters long")

    def accountTypeValidator(self, userId, usertype):
        identifier = str(userId)[:3]
        print(f" the first three are: {identifier}")
        if identifier == "233" and usertype != "Student":
            self.alert.append("You are a student, please create a student account")
        elif identifier == "412" and usertype != "Coordinator":
            self.alert.append("You are staff, please create a staff account")
        elif identifier not in ["233", "412"]:
            self.alert.append("Invalid Id")

    def passwordValidator(self, password1, password2):
        regex = r'^(?=.*[$%&@!€])(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[A-Za-z0-9$%&@!€]{8,16}'
        
        if password1 != password2:
            self.alert.append("Passwords do not match")
            return
        else:
            if len(password1) < 8 or len(password1) > 16:
                self.alert.append("Your password must be between 8 and 18 characters")
            if not re.search(r'[$%&@!€]', password1):
                self.alert.append("Your password needs at least one special character")
            if not re.search(r'[0-9]', password1):
                self.alert.append("Your password needs at least one number")
            if not re.search(r'[A-Za-z]', password1):
                self.alert.append("Your password needs both upper and lowercase letters")
    
    def emailValidator(self, email):
        regex = r'^[a-zA-Z0-9._-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,4}$'
        
        if not re.match(regex, email):
            self.alert.append("Invalid email")
        
    def usernameValidator(self, username):
        numbers = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
        username = str(username)
        if len(username) < 8:
            self.alert.append("Username must be at least 8 characters long")
            return
        
        for c in username:
            if c in numbers:
                return
        self.alert.append("Username must contain at least one number")