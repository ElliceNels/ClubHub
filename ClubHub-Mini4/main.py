from flask import Flask, render_template, request
from Login import Login


# Provide template folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route('/')
@app.route('/index.html')
def index():
    return render_template('index.html')

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
def signupValidation():
    
        if request.method == "POST":
            firstname = request.form.get("firstnamebar").strip()
            lastname  = request.form.get("lastnamebar").strip()
            userId = request.form.get("IDbar").strip()
            email = request.form.get("emailbar").strip()
            phonenumber = request.form.get("phonenumberbar").strip()
            username = request.form.get("usernamebar").strip()
            password1 = request.form.get("password1bar").strip()
            password2 = request.form.get("password2bar").strip()
            usertype = request.form.get("usertype").strip()
        
        SignUpValidator = Login()
        alerts = SignUpValidator.signupValidation( firstname, lastname, userId, email, phonenumber, username,password1, password2, usertype)
        if alerts == []:
            return(render_template("index.html"))
        else:
            return(render_template('signup.html', warning=alerts))
        
@app.route('/LoginProcess_Form', methods=["POST"])
def LoginValidation():
    if request.method == "POST":
        password1 = request.form.get("passwordbar").strip()
        password2 = request.form.get("confirmpasswordbar").strip()

        LoginValidator = Login()
        alerts = LoginValidator.doPasswordsMatch(password1, password2)
        print(password1, password2)
        print(alerts)
        if alerts == []:
             return render_template('index.html')
        else:
            return render_template('login.html', warning=alerts)

    
        

if __name__ == '__main__':
    app.run(debug=True)
