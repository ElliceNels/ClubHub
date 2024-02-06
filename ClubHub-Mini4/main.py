from flask import Flask, render_template

# Provide template folder name
app = Flask(__name__, template_folder='TemplateFiles', static_folder='StaticFiles')


clubs = [
    {"name": "Club 1", "description": "Description for Club 1", "coordinator_name": "John Doe"},
    {"name": "Club 2", "description": "Description for Club 2", "coordinator_name": "Jane Doe"},
    {"name": "Club 3", "description": "Description for Club 3", "coordinator_name": "Bob Smith"},
]
club_members = ["Alice Smith", "Bob Johnson", "Charlie Brown", "David Miller", "Eva Garcia", 
                "Frank Robinson", "Grace Lee", "Henry Davis", "Ivy Chen", "Jack Wilson", "Kelly Turner",
                "Leo Martinez"]


@app.route('/')
def index():
    return render_template('clubs_display.html', clubs=clubs)

@app.route('/create_club')
def create_club():
    return render_template('create_club.html')

@app.route('/club_mainpage')
def club_mainpage():
    return render_template('/club_mainpage.html', club_members=club_members)

if __name__ == '__main__':
    app.run(debug=True)
