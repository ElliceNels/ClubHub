from flask import Flask, render_template, request
from LoginValidation import LoginValidation
from LoginVerification import LoginVerification
from Verification import Verification

# Provide template folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')

clubs = [
    {"name": "Club 1", "description": "Description for Club 1", "coordinator_name": "John Doe"},
    {"name": "Club 2", "description": "Description for Club 2", "coordinator_name": "Jane Doe"},
    {"name": "Club 3", "description": "Description for Club 3", "coordinator_name": "Bob Smith"},
]
club_members = ["Alice Smith", "Bob Johnson", "Charlie Brown", "David Miller", "Eva Garcia",
                "Frank Robinson", "Grace Lee", "Henry Davis", "Ivy Chen", "Jack Wilson", "Kelly Turner",
                "Leo Martinez"]

isCoord = False

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/LoginProcess_Form', methods=["POST"])
def loginValidationRoute():
    global isCoord
    if request.method == "POST":
        User_id = request.form.get("IDbar").strip()
        isCoord = Verification.isCoord(User_id)
        Username = request.form.get("usernamebar").strip()
        password1 = request.form.get("password1bar").strip()
        password2 = request.form.get("password2bar").strip()

        loginValidator = LoginValidation()
        alerts = loginValidator.doPasswordsMatch(password1, password2)

        if alerts == []:
            loginVerifier = LoginVerification()
            if loginVerifier.Login(User_id, Username, password1):
                approvalStatus = loginVerifier.approvalStatus(User_id)
                if approvalStatus == True:
                    return EventMain()
                else:
                    return render_template('postLogin.html', approvalmessage=approvalStatus)
            else:
                return render_template('login.html', warning=loginVerifier.alert)
        else:
            return render_template('login.html', warning=alerts)



@app.route('/clubs_display')
def clubs_display():
    return render_template('clubs_display.html', clubs=clubs)


@app.route('/create_club')
def create_club():
    return render_template('create_club.html')


User_id = 4121234


@app.route('/Profile')
def Profile():
    if coord:
        return render_template('ProfileCoord.html')
    else:
        return render_template('ProfileStud.html')


@app.route('/Inbox')
def Inbox():
    return render_template('Inbox.html')


@app.route('/UpdateProfile')
def UpdateProfile():
    if Verification.isCoord(User_id=User_id):
        return render_template('UpdateProfileCoord.html')
    else:
        return render_template('UpdateProfileStud.html')


@app.route("/EventMain")
def EventMain():
    return render_template('EventMain.html')


@app.route("/EventDetails")
def EventDetails():
    return render_template('EventDetails.html')


@app.route("/CreateEvents")
def CreateEvents():
    return render_template('CreateEvents.html')


@app.route('/club_mainpage')
def club_mainpage():
    return render_template('/club_mainpage.html', club_members=club_members)


# Provide template folder name


@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.route('/signup.html')
def signUp():
    return render_template('signup.html')


@app.route('/login.html')
def login():
    return render_template('login.html')


@app.route('/SignUpProcess_Form', methods=["POST"])
def signupValidationRoute():
    if request.method == "POST":
        firstname = request.form.get("firstnamebar").strip()
        lastname = request.form.get("lastnamebar").strip()
        userId = request.form.get("IDbar").strip()
        email = request.form.get("emailbar").strip()
        phonenumber = request.form.get("phonenumberbar").strip()
        username = request.form.get("usernamebar").strip()
        password1 = request.form.get("password1bar").strip()
        password2 = request.form.get("password2bar").strip()
        usertype = request.form.get("usertype")
        print(usertype)

        signUpValidator = LoginValidation()
        alerts = signUpValidator.signupValidation(firstname, lastname, userId, email, phonenumber, username, password1,
                                                  password2, usertype)
        if alerts == []:
            signUpVerfier = LoginVerification()
            if signUpVerfier.SignUp(userId, username, phonenumber, password1, firstname, lastname, email, usertype):
                return render_template('login.html')
            else:
                return render_template('signup.html', warning=signUpVerfier.alert)
        else:
            return render_template('signup.html', warning=alerts)




if __name__ == '__main__':
    app.run(debug=True)

# USEFUL FOR CLEAR VALUES
# for row in username:
#    for column in row:
#       print(column)
