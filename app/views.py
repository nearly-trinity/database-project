from app import app
from flask import flash, Flask, render_template


@app.route("/")
def home():
    games = [
        {"id": 1, "home_team": "Trinity", "away_team": "Southwestern", "sport": "Football", "date": "Nov 13", "time": "7PM"},
        {"id": 2, "home_team": "Trinity", "away_team": "UT Dallas", "sport": "Volleyball", "date": "Nov 14", "time": "6PM"},
        {"id": 3, "home_team": "Trinity", "away_team": "Hardin-Simmons", "sport": "Track and Field", "date": "Nov 18", "time": "11AM"},
    ]
    return render_template("home.html", games=games)

@app.route("/team")
def team():
    return render_template("team.html")

@app.route("/leaderboard")
def leaderboard():
    return render_template("leaderboard.html")