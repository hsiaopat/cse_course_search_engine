
from flask import Flask

app = Flask(__name__)

@app.route("/")
def hello_world():
    return "<p>Hello, World!</p>"

#to run --> flask run -h 0.0.0.0 -p 9000
