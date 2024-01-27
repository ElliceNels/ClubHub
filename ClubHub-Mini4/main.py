from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return """
    <html>
    <head>
        <style>
            h1 {
            color: #996633;
            text-align: center;
            font-size: 28px;
            }

            p {
            font-family: verdana;
            font-size: 18px;
            text-align: center;
            }
        </style>
    </head>
    <body>
        <h1>ClubHub Online</h1>
        <p>This is the Offical webpage of ClubHub.<p>
        <p>Rights of this website are accredited to 'Ellice', 'Michelle', 'Kelly', 'Alisia'.
    </body>
    </html>
    """