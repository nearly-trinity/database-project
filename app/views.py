from app import app
from flask import flash


@app.route("/")
def helloworld():
    return "Hello World"
