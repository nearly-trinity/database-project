from app import app
from flask import flash


@app.route("/")
def helloworld():
    flash("test", "success")
    return "Hello World"
