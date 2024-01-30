from flask import Flask, render_template

# Provide template folder name
app = Flask(__name__, template_folder='TemplateFiles', static_folder='StaticFiles')

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)