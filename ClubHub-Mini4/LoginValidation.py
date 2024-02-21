import re
from constants import DB_PATH


class Login_validation:
    def __init__(self):
        self.alert = []

    def signup_validation(self, first_name, last_name, user_id, email, phone_number, user_name, password1, password2, user_type):
        self.name_validator(first_name, last_name)
        self.account_type_validator(user_id, user_type)
        self.username_validator(user_name)
        self.password_validator(password1, password2)
        self.email_validator(email)
        self.phone_number_validator(phone_number)
        print("Has gone through all the steps")
        return self.alert

    def name_validator(self, first_name, last_name):
        print("Has reached name")
        first_name = first_name.strip()
        last_name = last_name.strip()
        if len(first_name) <= 2 or len(last_name) <= 2:
            self.alert.append("First name and last name must both be at least 2 characters long")

    def account_type_validator(self, user_id, user_type):
        print("Has reached acc type")
        if str(user_id).isdigit() == False:
            self.alert.append("User id must only contain numbers")
            return
        if len(str(user_id)) != 7:
            self.alert.append("User id must be 7 numbers long")
        identifier = str(user_id)[:3]
        if identifier == "233" and user_type != "Student":
            self.alert.append("You are a student, please create a student account")
        elif identifier == "412" and user_type != "Coordinator":
            self.alert.append("You are staff, please create a staff account")
        elif identifier not in ["233", "412"]:
            self.alert.append("Invalid Id")

    def password_validator(self, password_1, password_2):
        print("Has reached password")
        regex = r'^(?=.*[$%&@!€_-?/\£])(?=.*[0-9])(?=.*[a-z])(?=.*[A-Z])[A-Za-z0-9$%&@!€]{8,16}'
        
        if password_1 != password_2:
            self.alert.append("Passwords do not match")
            return
        else:
            if len(password_1) < 8 or len(password_1) > 16:
                self.alert.append("Your password must be between 8 and 18 characters")
            if not re.search(r'[$%&@!€]', password_1):
                self.alert.append("Your password needs at least one special character")
            if not re.search(r'[0-9]', password_1):
                self.alert.append("Your password needs at least one number")
            if not re.search(r'[A-Za-z]', password_1):
                self.alert.append("Your password needs both upper and lowercase letters")
    
    def email_validator(self, email):
        print("Has reached email")
        regex = r'([A-Za-z0-9]+[.-_])*[A-Za-z0-9]+@[A-Za-z0-9-]+(\.[A-Za-z]{2,})+'
        
        if not re.search(regex, email):
            self.alert.append("Invalid email")
        
    def username_validator(self, user_name):
        print("Has reached username")
        regex = "^[A-Za-z0-9_-]*$"
        if len(user_name) < 8:
            self.alert.append("Username must be at least 8 characters long")
            return

        if not re.search(regex, user_name):
            self.alert.append("Username must contain at least one number")
            
    def phone_number_validator(self, phone_number):
        
        try:
            int(phone_number[1:])
            int(str(phone_number[0]))
        except ValueError as e:
            self.alert.append("Phone number must be a number")
            return
        if len(str(phone_number)) != 10:
            self.alert.append("Irish phone numbers must be 10 digits long")
            
    def do_passwords_match(self, password_1, password_2):
        if password_1 != password_2:
            self.alert.append("Passwords dont match")
        return self.alert