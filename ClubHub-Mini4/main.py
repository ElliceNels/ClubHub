
from flask import Flask, render_template, request, redirect, url_for
from LoginValidation import LoginValidation
from LoginVerification import LoginVerification
from datetime import datetime, timedelta
from Admin import Admin


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


@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

@app.route('/clubs_displayStud')
def clubs_displayStud():
    return render_template('clubs_displayStud.html', clubs=clubs)

@app.route('/clubs_displayCoord')
def clubs_displayCoord():
    return render_template('clubs_displayCoord.html', clubs=clubs)

@app.route('/Admin')
def showAdmin():
    AdminInfo = Admin()
    userList = AdminInfo.getUserList(1,0)
    return render_template('Admin.html', userList = userList)

@app.route('/ApprovedUsers')
def showApprovedUsers():
    AdminInfo = Admin()
    userList = AdminInfo.getUserList(0,1)
    return render_template('ApprovedUsers.html',userList=userList)

@app.route('/approvalform', methods=["POST"])
def approvalFormRoute():
    if request.method == "POST":
        status = int(request.form.get("status"))
        User_id = int(request.form.get("user"))
        AdminManagement = Admin()
        AdminManagement.individualapproveOrReject(User_id, status)
        return redirect(url_for('showAdmin'))

@app.route('/deletionform', methods=["POST"])
def deletionFormRoute():
    if request.method == "POST":
        status = int(request.form.get("status"))
        User_id = int(request.form.get("user"))
        AdminManagement = Admin()
        AdminManagement.individualapproveOrReject(User_id, status)
        return redirect(url_for('showApprovedUsers'))
    
@app.route('/massapprovalform', methods=["POST"])
def massApprovalFormRoute():
    if request.method == "POST":
        status = int(request.form.get("status"))
        
        AdminManagement = Admin()
        AdminManagement.massapproveOrReject(status)
        return redirect(url_for('showAdmin'))
 
    
@app.route('/create_club')
def create_club():
    return render_template('create_club.html')


@app.route('/ProfileStud')
def ProfileStud():
    return render_template('ProfileStud.html')

@app.route("/ProfileCoord")
def ProfileCoord():
    return render_template('ProfileCoord.html')

@app.route('/Inbox')
def Inbox():
    return render_template('Inbox.html')



@app.route('/UserDetails', methods=["POST"])
def  UserDetails():
    if request.method =="POST":
        UserID = request.form.get("userdeets")
        UserInfo = Admin()
        userinformation = UserInfo.getUserDetails(UserID)
        return render_template('UserDetails.html', userinformation=userinformation)

@app.route('/UpdateProfileStud')
def UpdateProfileStud():
    return render_template('UpdateProfileStud.html')


@app.route('/UpdateProfileCoord')
def UpdateProfileCoord():
    return render_template('UpdateProfileCoord.html')



@app.route("/EventDetails")
def EventDetails():
    return render_template('EventDetails.html')


@app.route("/CreateEvents")
def CreateEvents():
    return render_template('CreateEvents.html')


@app.route("/EventMain")
def EventMain():
    dates = [datetime.now() + timedelta(days=i) for i in range(16)]
    return render_template('EventMain.html', dates=dates)

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
        alerts = signUpValidator.signupValidation(firstname, lastname, userId, email, phonenumber, username, password1, password2, usertype)
        if alerts == []:
            signUpVerfier = LoginVerification()
            if signUpVerfier.SignUp(userId, username, phonenumber, password1, firstname, lastname, email, usertype):
                return render_template('login.html')
            else:
                return render_template('signup.html', warning=signUpVerfier.alert)
        else:
            return render_template('signup.html', warning=alerts)
        
@app.route('/LoginProcess_Form', methods=["POST"])
def loginValidationRoute():
    if request.method == "POST":
        User_id = request.form.get("IDbar").strip()
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
                    redirect(url_for('EventMain'))
                else:
                    return render_template('postLogin.html', approvalmessage=approvalStatus)
            else:
                return render_template('login.html', warning=loginVerifier.alert)
        else:
            return render_template('login.html', warning=alerts)

    
        

if __name__ == '__main__':
    app.run(debug=True)
