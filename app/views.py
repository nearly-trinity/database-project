from app import app
from flask import flash, Flask, render_template, request, session
import json

@app.route("/")
def home():
    games = [
        {"id": "1", "home_team": "Trinity", "away_team": "Southwestern", "sport": "Football", "date": "Nov 13", "time": "7PM"},
        {"id": "2", "home_team": "Trinity", "away_team": "UT Dallas", "sport": "Volleyball", "date": "Nov 14", "time": "6PM"},
        {"id": "3", "home_team": "Trinity", "away_team": "Hardin-Simmons", "sport": "Track and Field", "date": "Nov 18", "time": "11AM"},
    ]

    return render_template("home.html", games=games)

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")

@app.route("/submit_votes", methods=['POST'])
def submit_votes():
    username = request.form.get('username')
    session['username'] = username

    games = request.form.get('games')
    games = json.loads(games) if games else []

    selected_options = {}
    for game in games:
        selected_options[game['id']] = request.form.get(f"{game['id']}", None)

    return render_template("leaderboard.html", username=username, selections=selected_options)


@app.route("/login")
def loginPage():
    return "login here"


@app.route("/test/<name>")
def testArgument(name=None):
    return "testing if the name works: " + str(name)
