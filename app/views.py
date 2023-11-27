from app import app
from flask import flash


@app.route("/")
def helloworld():
    return "Hello World"


@app.route("/login")
def loginPage():
    return "login here"


@app.route("/test/<name>")
def testArgument(name=None):
    return "testing if the name works: " + str(name)
