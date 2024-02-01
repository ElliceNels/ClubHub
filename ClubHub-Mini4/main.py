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

@app.route('/process_form', methods=["POST"])
def signupValidation():
    
        if request.method == "POST":
            firstname = request.form.get("firstnamebar")
            lastname  = request.form.get("lastnamebar")
            userId = request.form.get("IDbar")
            email = request.form.get("emailbar")
            username = request.form.get("usernamebar")
            password1 = request.form.get("password1bar")
            password2 = request.form.get("password2bar")
            usertype = request.form.get("usertype") 
        
        loginValidator = Login()
        alerts = loginValidator.signupValidation( firstname, lastname, userId, email, username,password1, password2, usertype)
        if alerts == []:
            return(render_template("index.html"))
        else:
            return(render_template('signup.html', warning=alerts))
        return(render_template('signup.html', warning=""))
        

if __name__ == '__main__':
    app.run(debug=True)
