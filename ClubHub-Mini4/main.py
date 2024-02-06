from flask import Flask, render_template

# Provide template folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route('/')
def index():
    return render_template('ProfileStud.html')

@app.route('/ProfileStud')
def ProfileStud():
    return render_template('ProfileStud.html')

@app.route("/ProfileCoord")
def ProfileCoord():
    return render_template('ProfileCoord.html')

@app.route('/Inbox')
def Inbox():
    return render_template('Inbox.html')

@app.route('/UpdateProfileStud')
def UpdateProfileStud():
    return render_template('UpdateProfileStud.html')


@app.route('/UpdateProfileCoord')
def UpdateProfileCoord():
    return render_template('UpdateProfileCoord.html')

@app.route("/Clubs")
def Clubs():
    return render_template('Clubs.html')


@app.route("/Events")
def Events():
    return render_template('Events.html')


if __name__ == '__main__':
    app.run(debug=True)
