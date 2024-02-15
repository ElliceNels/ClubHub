import re
from constants import DB_PATH


class LoginValidation:
    def __init__(self):
        self.alert = []

    def signupValidation(self, firstname, lastname, userId, email, phonenumber, username, password1, password2, usertype):
        self.nameValidator(firstname, lastname)
        self.accountTypeValidator(userId, usertype)
        self.usernameValidator(username)
        self.passwordValidator(password1, password2)
        self.emailValidator(email)
        self.phonenumberValidator(phonenumber)
        return self.alert

    def nameValidator(self, firstname, lastname):
        firstname = firstname.strip()
        lastname = lastname.strip()
        if len(firstname) <= 2 or len(lastname) <= 2:
            self.alert.append("First name and last name must both be at least 2 characters long")

    def accountTypeValidator(self, userId, usertype):
        if str(userId).isdigit() == False:
            self.alert.append("User id must only contain numbers")
            return
        if len(str(userId)) != 7:
            self.alert.append("User id must be 7 numbers long")
        identifier = str(userId)[:3]
        print(f" the first three are: {identifier}")
        if identifier == "233" and usertype != "Student":
            self.alert.append("You are a student, please create a student account")
        elif identifier == "412" and usertype != "Coordinator":
            self.alert.append("You are staff, please create a staff account")
        elif identifier not in ["233", "412"]:
            self.alert.append("Invalid Id")

    def passwordValidator(self, password1, password2):
        regex = r'^(?=.*[$%&@!€_-?/\£])(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[A-Za-z0-9$%&@!€]{8,16}'
        
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
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+'
        
        if not re.search(regex, email):
            self.alert.append("Invalid email")
        
    def usernameValidator(self, username):
        regex = "^[A-Za-z0-9_-]*$"
        if len(username) < 8:
            self.alert.append("Username must be at least 8 characters long")
            return

        if not re.search(regex, username):
            self.alert.append("Username must contain at least one number")
    def phonenumberValidator(self, phonenumber):
        try:
            int(phonenumber[1:])
            int(str(phonenumber[0]))
        except ValueError as e:
            self.alert.append("Phone number must be a number")
            return
        if len(str(phonenumber)) != 10:
            self.alert.append("Irish phone numbers must be 10 digits long")
            
    def doPasswordsMatch(self, password1, password2):
        if password1 != password2:
            self.alert.append("Passwords dont match")
        return self.alert