from flask import Flask, render_template

# Provide template folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route('/')
def index():
    return render_template('ProfileStud.html')

#@app.route("/Profile")
#def Clubs():
#    return render_template('ProfileStud.html')

@app.route('/Inbox')
def Inbox():
    return render_template('Inbox.html')

@app.route('/UpdateProfile')
def UpdateProfile():
    return render_template('UpdateProfile.html')


@app.route("/Clubs")
def Clubs():
    return render_template('Clubs.html')


@app.route("/Events")
def Events():
    return render_template('Events.html')


if __name__ == '__main__':
    app.run(debug=True)
