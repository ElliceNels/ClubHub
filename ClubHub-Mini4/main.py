from flask import Flask, render_template

# Provide template folder name
app = Flask(__name__, template_folder='templateFiles', static_folder='staticFiles')


@app.route('/')
@app.route('/Inbox')
def index():
    return render_template('Inbox.html')


@app.route("/Clubs")
def Clubs():
    return render_template('Clubs.html')


@app.route("/Events")
def Events():
    return render_template('Events.html')


if __name__ == '__main__':
    app.run(debug=True)
