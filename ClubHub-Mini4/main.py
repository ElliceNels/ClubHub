from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
    <html>
    <head>
    </head>
    <body>
        <h1>ClubHub Online</h1>
    </body>
    </html>
    """