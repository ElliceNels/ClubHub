import re
from constants import DB_PATH


class Login_validation:
    def __init__(self):
        self.alert = []

    def signup_validation(self, first_name, last_name, user_id, email, phone_number, user_name, password1, password2, user_type):
        self.name_validator(first_name)
        self.name_validator(last_name)
        self.account_type_validator(user_id, user_type)
        self.username_validator(user_name)
        self.password_validator(password1, password2)
        self.email_validator(email)
        self.phone_number_validator(phone_number)
        return self.alert

    def name_validator(self, name):
        # ensure the name isn't just a character
        name = name.strip()
        if len(name) <= 2:
            self.alert.append("name fields must be at least 2 characters long")

    def account_type_validator(self, user_id, user_type):
        #must exactly 7 digits
        if len(str(user_id)) != 7:
            self.alert.append("User id must be 7 numbers long")
        identifier = str(user_id)[:3]
        # all of this ensures that the user id matches the account they are trying to create
        if identifier == "233" and user_type != "Student":
            self.alert.append("You are a student, please create a student account")
        elif identifier == "412" and user_type != "Coordinator":
            self.alert.append("You are staff, please create a staff account")
        elif identifier not in ["233", "412"]:
            self.alert.append("Invalid Id")
            
    def passwords_match(self, password_1, password_2):
        return password_1 == password_2
    
    def password_requirements(self, password_1):
        # enforces password requirments
         if len(password_1) < 8 or len(password_1) > 16:
            self.alert.append("Your password must be between 8 and 18 characters")
         if not re.search(r'[$%&@!€_\-\?/\£#+*()]', password_1):
            self.alert.append("Your password needs at least one special character")
         if not re.search(r'[0-9]', password_1):
            self.alert.append("Your password needs at least one number")
         if not re.search(r'[A-Za-z]', password_1):
            self.alert.append("Your password needs both upper and lowercase letters")
    

    def password_validator(self, password_1, password_2):
        try:
            if not self.passwords_match(password_1, password_2):
                self.alert.append("Passwords do not match")
            else:
                self.password_requirements(password_1)
        except Exception as e:
            print(f"An error occurred during password validation: {e}")
            
    
    def email_validator(self, email):
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+'
        
        if not re.search(regex, email):
            self.alert.append("Invalid email")
        
    def username_validator(self, user_name):
        regex = "^[A-Za-z0-9_-]*$"
        if len(user_name) < 8:
            self.alert.append("Username must be at least 8 characters long")
        elif not re.search(regex, user_name):
            self.alert.append("Username invalid")
            
    def phone_number_validator(self, phone_number):
        try:
            int(phone_number[1:])
            int(str(phone_number[0]))
        except ValueError as e:
            print(f"An error occured while validating phone number: {e}")
            self.alert.append("Phone number must be a number")
            return
        if len(str(phone_number)) != 10:
            self.alert.append("Irish phone numbers must be 10 digits long")
            
 