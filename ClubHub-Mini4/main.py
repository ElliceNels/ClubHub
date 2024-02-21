import sqlite3

from flask import Flask, render_template, request, redirect, url_for
from databaseHandling import db_startup
from LoginValidation import Login_validation
from LoginVerification import Login_verification
from Verification import Verification
from datetime import datetime, timedelta
from session import Session
from Admin import Admin
from EventsRegister import register_events
from Club import ClubCreationVerification, ClubDeletion
from Coordinator import Coordinator
from ClubInbox import ClubInbox
from User import User
from EventsInbox import EventsInbox
from constants import DB_PATH
from EventMainPage import eventsmainpage, eventDetails, club_info, signup_event

# Provide template folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')
app.secret_key = 'who_would_have_thought_teehee'
# session to store user_id for time logged in
user_session = Session()

# creates database if not existing
db_startup()

@app.route('/')
@app.route('/index')
def index():
    print(user_session.getUser_id())
    return render_template('index.html')



@app.route('/signup.html')
def signUp():
    return render_template('signup.html')


@app.route('/login.html')
def login():
    return render_template('login.html')




@app.route('/LoginProcess_Form', methods=["POST"])
def login_validation_route():
    if request.method == "POST":
        user_name = request.form.get("usernamebar").strip()
        password_1 = request.form.get("password1bar").strip()
        login_verifier = Login_verification()
        user_id = login_verifier.get_user_id_from_username(user_name)
        if user_id != False:
            if login_verifier.Login(user_id, user_name, password_1):
                approval_status = login_verifier.approval_status(user_id)
                if approval_status == True:
                    user_session.login(user_id)

                    print(user_session.isAdministrator())
                    return EventMain()
                else:
                    return render_template('postLogin.html', approvalmessage=approval_status)
            else:
                return render_template('login.html', warning=login_verifier.alert)
        else:
            return render_template('login.html', warning="Account does not exist")


@app.route('/SignUpProcess_Form', methods=["POST"])
def signupValidationRoute():
    if request.method == "POST":
        first_name = request.form.get("firstnamebar").strip()
        last_name = request.form.get("lastnamebar").strip()
        user_id = request.form.get("IDbar").strip()
        email = request.form.get("emailbar").strip()
        phone_number = request.form.get("phonenumberbar").strip()
        user_name = request.form.get("usernamebar").strip()
        password_1 = request.form.get("password1bar").strip()
        password_2 = request.form.get("password2bar").strip()
        user_type = request.form.get("usertype")

        sign_up_validator = Login_validation()
        alerts = sign_up_validator.signup_validation(first_name, last_name, user_id, email, phone_number, user_name, password_1,
                                                     password_2, user_type)
        if alerts == []:
            sign_up_verfier = Login_verification()
            if sign_up_verfier.Sign_up(user_id, user_name, phone_number, password_1, first_name, last_name, email, user_type):
                return redirect(url_for('login'))
            else:
                return render_template('signup.html', warning=sign_up_verfier.alert)
        else:
            return render_template('signup.html', warning=alerts)
        

@app.route('/logout')
def user_logout():
    user_session.logout()
    return redirect(url_for('index'))


##############################################################################Clubs##############################################################################

@app.route('/club_mainpage/<club_name>', methods=["GET", "POST"])
def club_mainpage(club_name):

    club_member_info = Coordinator.display_members(club_name)

    if Verification.coordinatingClub(club_name, user_session.getUser_id()) == club_name:

        if request.method == "POST":

            club_name = request.form.get("delete_club")
            ClubDeletion.deleteClub(club_name)

            return redirect(url_for('clubs_display'))

        return render_template('/club_mainpage.html', club_member_info=club_member_info, club_name=club_name)
    
    if user_session.isAdministrator():
        return render_template('/club_mainpage.html', club_member_info=club_member_info, club_name=club_name)
    
    return clubs_display()


@app.route('/clubs_display', methods=["GET", "POST"])
def clubs_display():
    # checks if user is a coordinator or an admin.
    if user_session.isCoordinator() or user_session.isAdministrator():

        if request.method == "POST":
            club_name = request.form.get("club_link")
        return render_template('clubs_displayCoord.html', clubs=Coordinator.get_club_data())
    
    else:
        if request.method == "POST":
            club_name = request.form.get("club_name")
            user_id = user_session.getUser_id()
            if not Coordinator.check_club_requests(user_id, club_name):
                Coordinator.request_club_membership(user_id, club_name)

        return render_template('clubs_displayStud.html', clubs=Coordinator.get_club_data())


@app.route('/create_club', methods=('GET', 'POST'))
def create_club():

    if not user_session.isAdministrator():
        if request.method == 'POST':

            # get data from html from to create a new club
            club_name = request.form['club-name']
            club_description = request.form['description']
            ClubCreationVerification.create_new_club(club_name, club_description, user_session.getUser_id())
        else:
            # if user has a club, display warning
            print('you have a club.')

    return render_template('create_club.html')


##############################################################################Profile##############################################################################

@app.route('/UpdateProfileStud')
def updateStudentProfileDisplay():
    return render_template('UpdateProfileStud.html')


@app.route('/changeDetails', methods=["POST"])
def changeDetailsRoute():
    if request.method == "POST":
        new_value = request.form.get("newvalue")
        column = request.form.get("column")
        user_id = user_session.getUser_id()
        table = None
        if column == "Username":
            table = "USER_LOGIN"
        else:
            table = "USER_DETAILS"
        user_information_handler = User()
        user_information_handler.update_user_information(table, column, new_value, user_id)
        return redirect(url_for('updateStudentProfileDisplay'))


@app.route('/Profile')
def Profile():
    details = Verification.profileDetails(user_session.getUser_id())

    if user_session.isCoordinator() or user_session.isAdministrator():
        club_owned = Verification.coordinatingClub(user_session.getUser_id(), user_session.getUser_id())
        return render_template('ProfileCoord.html', details=details, clubOwned=club_owned)
    else:
        club_membership = Verification.clubMemberships(user_session.getUser_id())
        return render_template('ProfileStud.html', details=details, clubMembership=club_membership)


@app.route('/UpdateProfile')
def UpdateProfile():
    if user_session.isCoordinator() or user_session.isAdministrator():
        return render_template('UpdateProfileCoord.html')
    else:
        return render_template('UpdateProfileStud.html')


##############################################################################Admin ClubInbox##############################################################################
@app.route('/Admin')
def showAdmin():
    admin_info = Admin()
    user_list = admin_info.get_user_list(1, 0)
    return render_template('Admin.html', userList=user_list)


@app.route('/approvalform', methods=["POST"])
def approvalFormRoute():
    if request.method == "POST":
        user_id = int(request.form.get("user"))
        admin_management = Admin()
        admin_management.individual_approve(user_id)
        return redirect(url_for('showAdmin'))
 
@app.route('/predeletionform', methods=["POST"])
def predeletionformroute():
    if request.method == "POST":
        user_id = int(request.form.get("user"))
        admin_management = Admin()
        admin_management.individual_reject(user_id)
        return redirect(url_for('showAdmin'))
        


@app.route('/postdeletionform', methods=["POST"])
def postdeletionFormRoute():
    if request.method == "POST":
        user_id = int(request.form.get("user"))
        admin_management = Admin()
        admin_management.individual_reject(user_id)
        return redirect(url_for('showApprovedUsers'))


@app.route('/ApprovedUsers')
def showApprovedUsers():
    admin_info = Admin()
    user_list = admin_info.get_user_list(0, 1)
    return render_template('ApprovedUsers.html', userList=user_list)


@app.route('/massapprovalform', methods=["POST"])
def massApprovalFormRoute():
    if request.method == "POST":
        status = int(request.form.get("status"))
        admin_management = Admin()
        admin_management.mass_approve(status)
        return redirect(url_for('showAdmin'))


@app.route('/UserDetails', methods=["POST"])
def UserDetails():
    if request.method == "POST":
        user_id = request.form.get("userdeets")
        user_info = Admin()
        user_information = user_info.get_user_details(user_id)
        return render_template('UserDetails.html', userinformation=user_information)
    
@app.route('/UserClubs', methods=["POST"])
def UserClubsRoute():
    if request.method == "POST":
        user_id = request.form.get("user")
        club_membership = Verification.clubMemberships(user_id)
        if club_membership == None:
            return redirect(url_for('showApprovedUsers'))
        else:
            return render_template('UserClubs.html', clubMembership=club_membership)



#########################################################################################ClubInbox#########################################################################

@app.route('/EventRequests')
def eventRequests():
    if user_session.isAdministrator():
        admin_info = Admin()
        user_list = admin_info.get_user_list(1, 0)
        return render_template('Admin.html', userList=user_list)
    elif user_session.isCoordinator():
        print("moving to inboxevents.html")
        event_requests = EventsInbox()
        club_waiting_list = event_requests.getEventWaitList(user_session.getUser_id(), 1)
        return render_template('InboxEvents.html', clubWaitingList=club_waiting_list)


@app.route('/ClubInbox')
def InboxRoute():
    print("in inbox")
    if user_session.isAdministrator():
        admin_info = Admin()
        user_list = admin_info.get_user_list(1, 0)
        return render_template('Admin.html', userList=user_list)
    elif user_session.isCoordinator():
        coord_info = ClubInbox()
        club_waiting_list = coord_info.clubApprovalList(user_session.getUser_id(), 1)
        return render_template('ClubInbox.html', clubWaitingList=club_waiting_list)


@app.route('/clubjoinform', methods=["POST"])
def clubJoinFormRoute():
    if request.method == "POST":
        status = int(request.form.get("status"))
        user_id = int(request.form.get("user"))
        inbox_info = ClubInbox()
        inbox_info.individualapproveOrReject(user_id, status)
        return redirect(url_for('InboxRoute'))


@app.route('/eventjoinform', methods=["POST"])
def eventJoinFormRoute():
    if request.method == "POST":
        status = int(request.form.get("status"))
        user_id = int(request.form.get("user"))
        event_join = EventsInbox()
        event_join.individualapproveOrRejectE(user_id, status)
        return redirect(url_for('InboxRoute'))


@app.route('/clubapprovalform', methods=["POST"])
def clubApprovalFormRoute():
    if request.method == "POST":
        status = int(request.form.get("status"))

        inbox_info = ClubInbox()
        inbox_info.massapprove(status)
        return redirect(url_for('InboxRoute'))


@app.route('/eventapprovalform', methods=["POST"])
def eventApprovalFormRoute():
    if request.method == "POST":
        status = int(request.form.get("status"))

        events_approval = EventsInbox()
        events_approval.massapproveE(status)
        return redirect(url_for('InboxRoute'))

@app.route('/memberremovalform', methods=["GET", "POST"])
def memberRemovalFormRoute():
    if request.method == "POST":
        status = int(request.form.get("status"))
        user_id = int(request.form.get("user"))
        inbox_info = ClubInbox()
        inbox_info.individualapproveOrReject(user_id, status)
        return redirect(url_for('clubMembers'))


##############################################################################Events###################################################################################

@app.route("/EventDetails/<int:event_id>" , methods=['GET', 'POST'])
def EventDetails(event_id):
    event_details = eventDetails(event_id)
    Club_id = event_details[0][5]
    club_info_data = club_info(Club_id)
    success_message = None
   
    if request.method == 'POST':
        user_id = user_session.getUser_id()
        if user_id:
            signup_event(Club_id, user_id, event_id)

            success_message = 'You have signed up for the event!'
            
    

    return render_template('EventDetails.html', event_details=event_details, club_info_data=club_info_data, success_message=success_message)


@app.route("/CreateEvents", methods=['GET', 'POST'])
def CreateEvents():
    warning_message = None
    success_message = None

    if request.method == 'POST':
        event_title = request.form.get('EventTitle').strip()
        description = request.form.get('Description').strip()
        date = request.form.get('Date').strip()
        time = request.form.get('Time').strip()
        venue = request.form.get('Venue').strip()

        if user_session.is_logged_in:
            user_id = user_session.getUser_id()
            if user_session.is_coord:
                try:
                    club_id = Verification.CoordinatorClubId(user_id)
                    if club_id:
                        event_datetime = datetime.strptime(f"{date} {time}", "%Y-%m-%d %H:%M")
                        event_date = event_datetime.date()
                        event_time = event_datetime.strftime("%H:%M")
                        register_events(event_title, description, event_date, event_time, venue, club_id)
                        success_message = "Event successfully created!!"
                    else:
                        warning_message = "You are not associated with any club!"
                except Exception as e:
                    warning_message = f"Error occurred: {e}"
            else:
                warning_message = "Only coordinators can create events."
        else:
            warning_message = "Please fill out all fields!!"
    return render_template('CreateEvents.html', warning=warning_message, success_message=success_message)


@app.route("/EventMain")
def EventMain():
    events = eventsmainpage()
    event_dates = [datetime.now() + timedelta(days=i) for i in range(16)]
    print(events)
    return render_template('EventMain.html', event_dates=event_dates, events=events, datetime=datetime)


def validate_event_form(EventTitle, Description, Date, Time, Venue):
    if not all([EventTitle, Description, Date, Time, Venue]):
        return False
    return True


@app.route('/UserDeets', methods=["POST"])
def UserDeets():
    if request.method == "POST":
        user_id = request.form.get("userdeets")
        user_info = Admin()
        user_information = user_info.get_user_details(user_id)
        return render_template('UserDetails.html', userinformation=user_information)


##############################################################################Error pages##############################################################################
@app.errorhandler(404)
def page_not_found(e):
    return render_template('error404.html'), 404


@app.errorhandler(AttributeError)
def handle_attribute_error(error):
    return render_template('attributeError.html'), 500


if __name__ == '__main__':
    app.run(debug=True)

# USEFUL FOR CLEAR VALUES
# for row in username:
#    for column in row:
#       print(column)
