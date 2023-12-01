from app import app
from flask import flash, Flask, render_template, request, session
import json

from datetime import datetime

# current date and time
date_time = datetime.now()

# format specification
format = '%Y-%m-%d at %H:%M:%S'

import sqlite3
con = sqlite3.connect('database.db', check_same_thread=False)
cur = con.cursor()

@app.route("/")
def home():
    games = cur.execute('''
        SELECT 
            SE.event_id,
            SE.event_name,
            SE.event_location,
            STRFTIME('%m/%d/%Y at %H:%M', event_date),
            T1.team_name AS home_team_name,
            T2.team_name AS away_team_name,
            SE.sport_type,
            SE.home_team_id,
            SE.away_team_id
        FROM SportingEvents SE
        JOIN Teams T1 ON SE.home_team_id = T1.team_id
        JOIN Teams T2 ON SE.away_team_id = T2.team_id
        WHERE SE.event_date >= date('now')
        ORDER BY SE.event_date
        ''')
    games = games.fetchall()
    print(games)
    
    return render_template("home.html", games=games)

@app.route("/team")
def team():
    team_id1 = request.args.get('team_id1')
    team_id2 = request.args.get('team_id2')
    print(team_id1)
    print(team_id2)

    home_team = cur.execute('''
        SELECT 
            first_name,
            last_name,
            position,
            jersey_number
        FROM Players
        WHERE team_id = ''' + team_id1 + '''    
    ''').fetchall()
    away_team = cur.execute('''
        SELECT 
            first_name,
            last_name,
            position,
            jersey_number
        FROM Players
        WHERE team_id = ''' + team_id2 + '''    
    ''').fetchall()
    
    return render_template("team.html", home=home_team, away=away_team)

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
        selected_options[game[0]] = request.form.get(f"{game[0]}", None)

    return render_template("leaderboard.html", username=username, selections=selected_options)


@app.route("/login")
def loginPage():
    return "login here"


@app.route("/test/<name>")
def testArgument(name=None):
    return "testing if the name works: " + str(name)
