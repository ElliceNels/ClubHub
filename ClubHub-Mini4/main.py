import sqlite3

from flask import Flask, render_template, request, redirect, url_for
from LoginValidation import LoginValidation
from LoginVerification import LoginVerification
from Verification import Verification
from datetime import datetime, timedelta
from session import Session 
from Admin import Admin
from EventsRegister import register_events
from Club import ClubCreationVerification
from Coordinator import Coordinator

from User import User


# Provide template folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.secret_key = 'who_would_have_thought_teehee'

club_members = ["Alice Smith", "Bob Johnson", "Charlie Brown", "David Miller", "Eva Garcia",
                "Frank Robinson", "Grace Lee", "Henry Davis", "Ivy Chen", "Jack Wilson", "Kelly Turner",
                "Leo Martinez"]

user_session = Session()

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')


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
                    user_session.login(User_id)
                    print(user_session.isAdministrator())
                    return EventMain()
                else:
                    return render_template('postLogin.html', approvalmessage=approvalStatus)
            else:
                return render_template('login.html', warning=loginVerifier.alert)
        else:
            return render_template('login.html', warning=alerts)




@app.route('/clubs_display')
def clubs_display():
    #checks if user is a coordinator or an admin.
    if user_session.isCoordinator() or user_session.isAdministrator():

        return render_template('clubs_displayCoord.html', clubs=Coordinator.get_club_data())
    else:

        return render_template('clubs_displayStud.html', clubs=Coordinator.get_club_data())
    
@app.route('/UpdateProfileStud')
def updateStudentProfileDisplay():
    return render_template('UpdateProfileStud.html')
    
@app.route('/changeDetails', methods=["POST"])
def changeDetailsRoute():
    if request.method == "POST":
        newvalue = request.form.get("newvalue")
        column = request.form.get("column")
        user_id = user_session.getUser_id()
        table = None
        if column == "Username":
            table = "USER_LOGIN"
        else:
            table = "USER_DETAILS"
        UserInformationHandler = User()
        UserInformationHandler.updateUserInformation(table, column, newvalue, user_id)
        return redirect(url_for('updateStudentProfileDisplay'))
    


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
 
    
@app.route('/create_club', methods=('GET', 'POST'))
def create_club():
    warning = None

    if request.method == 'POST':

        #get data from html from to create a new club
        club_name = request.form['club-name']
        club_description = request.form['description']
        ClubCreationVerification.create_new_club(club_name, club_description, user_session.getUser_id())
    else:

        #if user has a club, display warning
        print('you have a club.')
        warning = 'you have a club.'

    return render_template('create_club.html', warning=warning)



@app.route('/Profile')
def Profile():
    details = Verification.profileDetails(user_session.getUser_id())

    if user_session.isCoordinator() or user_session.isAdministrator():
        clubOwned = Verification.coordinatingClub(user_session.getUser_id(), user_session.getUser_id())
        return render_template('ProfileCoord.html', details=details, clubOwned=clubOwned)
    else:
        clubMembership = Verification.clubMemberships(user_session.getUser_id())
        return render_template('ProfileStud.html', details=details, clubMembership=clubMembership)

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


@app.route('/UpdateProfile')
def UpdateProfile():
    if user_session.isCoordinator() or user_session.isAdministrator():
        return render_template('UpdateProfileCoord.html')
    else:
        return render_template('UpdateProfileStud.html')

@app.route('/changeDetails', methods=['POST'])
def submit_form():
    User_id = user_session.getUser_id()
    firstname = request.form['Firstname']
    lastname = request.form['Lastname']
    username = request.form['Username']
    email = request.form['Email']
    phoneNum = request.form['Contact_number']

    print(User_id)
    print(firstname)
    print(lastname)
    print(username)
    print(email)
    print(phoneNum)

    conn = sqlite3.connect('ClubHub-Mini4/database/Clubhub.db')
    cursor = conn.cursor()

    cursor.execute('UPDATE USER_DETAILS SET Firstname = ?, Lastname = ?, Contact_number = ?, Email = ? WHERE User_id = ?', (firstname, lastname, phoneNum, email, User_id))
    cursor.execute('UPDATE USER_LOGIN SET Username = ? WHERE User_id = ?', (username, User_id))

    conn.commit()
    conn.close()

    return Profile()


@app.route("/EventDetails")
def EventDetails():
    return render_template('EventDetails.html')


def validate_event_form(EventTitle,Description, Date, Time, Venue):
    if not all([EventTitle, Description, Date, Time, Venue]):
        return False
    return True

@app.route("/CreateEvents" , methods=['POST'])
def CreateEvents():
    if request.method == 'POST':
        EventTitle = request.form.get('EventTitle').strip()
        Description = request.form.get('Description').strip()
        Date = request.form.get('Date').strip()
        Time = request.form.get('Time').strip()
        Venue = request.form.get('Venue').strip()


    if validate_event_form([EventTitle , Description , Date , Time , Venue]):
        event_datetime = datetime.strptime(f"{Date} {Time}", "%Y-%m-%d %H:%M")
        event_date = event_datetime.date()
        event_time = event_datetime.time()
        register_events(EventTitle, Description, event_date, event_time, Venue)
        return render_template('CreateEvents.html', EventTitle=EventTitle)
    else:
        return render_template('CreateEvents.html', warning="Please fill out all fields!!")

    return render_template('CreateEvents.html')


@app.route("/EventMain")
def EventMain():
    dates = [datetime.now() + timedelta(days=i) for i in range(16)]
    return render_template('EventMain.html', dates=dates)

@app.route('/club_mainpage')
def club_mainpage():

    return render_template('/club_mainpage.html', club_members=club_members)



@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404

@app.errorhandler(AttributeError)
def handle_attribute_error(error):
    return render_template('attributeError.html'), 500


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
