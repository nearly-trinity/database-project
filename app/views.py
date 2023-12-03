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
    
    return render_template("home.html", games=games)

@app.route("/team")
def team():
    team_id1 = request.args.get('team_id1')
    team_id2 = request.args.get('team_id2')
    game_id = request.args.get('game_id')

    game_info = cur.execute('''
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
        WHERE SE.event_id = ''' + game_id + ''';
    ''').fetchone()

    home_coach = cur.execute('''
        SELECT
            first_name,
            last_name
        FROM Coaches
        WHERE team_id = ''' + team_id1 + ''';
    ''').fetchone()
    
    away_coach = cur.execute('''
        SELECT
            first_name,
            last_name
        FROM Coaches
        WHERE team_id = ''' + team_id2 + ''';
    ''').fetchone()

    home_team = cur.execute('''
        SELECT 
            first_name,
            last_name,
            position,
            jersey_number
        FROM Players
        WHERE team_id = ''' + team_id1 + ''';  
    ''').fetchall()
    away_team = cur.execute('''
        SELECT 
            first_name,
            last_name,
            position,
            jersey_number
        FROM Players
        WHERE team_id = ''' + team_id2 + ''';    
    ''').fetchall()
    
    return render_template("team.html", home=home_team, away=away_team, game_info=game_info, home_coach=home_coach, away_coach=away_coach)


def get_user_votes(username):

    cur.execute("SELECT user_id FROM Users WHERE username=?", (username,))
    user_result = cur.fetchone()

    if user_result:
        user_id = user_result[0]

        cur.execute("""
            SELECT 
                SportingEvents.event_name,
                GameResults.home_team_score,
                GameResults.away_team_score,
                Teams.team_name AS chosen_winner,
                CASE
                    WHEN Teams.team_id = GameResults.winner_team_id THEN 1
                    ELSE 0
                END AS voted_correctly
            FROM 
                UserVotes
                JOIN SportingEvents ON UserVotes.event_id = SportingEvents.event_id
                JOIN GameResults ON UserVotes.event_id = GameResults.event_id
                JOIN Teams ON UserVotes.chosen_winner_id = Teams.team_id
            WHERE 
                UserVotes.user_id = ?
            ORDER BY SportingEvents.event_date DESC;
        """, (user_id,))

        votes_data = cur.fetchall()
        return votes_data

    return []




@app.route("/leaderboard")
def leaderboard():

    votes = get_user_votes(session['username'])

    users = cur.execute('''
        SELECT
            user.username,
            COUNT(CASE WHEN GR.event_id = UV.event_id THEN 1 ELSE 0 END) AS totalPredictions,
            SUM(CASE WHEN GR.winner_team_id = UV.chosen_winner_id THEN 1 ELSE 0 END) AS correctPredictions,
            SUM(CASE WHEN GR.winner_team_id = UV.chosen_winner_id THEN 1 ELSE 0 END * 100) / COUNT(CASE WHEN GR.event_id = UV.event_id THEN 1 ELSE 0 END) AS correctRatio
        FROM UserVotes UV
        JOIN Users user ON user.user_id = UV.user_id
        LEFT JOIN GameResults GR ON GR.event_id = UV.event_id
        GROUP BY UV.user_id, user.username
        ORDER BY correctRatio DESC;
    ''')

    
    return render_template("leaderboard.html", users=users, votes=votes)

@app.route("/submit_votes", methods=['POST'])
def submit_votes():
    username = request.form.get('username')
    session['username'] = username

    cur.execute("SELECT user_id FROM Users WHERE username=?", (username,))
    user_result = cur.fetchone()

    if user_result:
        user_id = user_result[0]
        print(user_id)

        games = request.form.get('games')
        games = json.loads(games) if games else []

        selected_options = {}
        for game in games:
            selected_options[game[0]] = request.form.get(f"{game[0]}", None)

        for event_id, chosen_winner in selected_options.items():
            if chosen_winner:
                cur.execute("SELECT sport_type FROM SportingEvents WHERE event_id=?", (event_id,))
                sport_type_result = cur.fetchone()
                if sport_type_result:
                    sport_type = sport_type_result[0]

                    cur.execute("""
                        INSERT INTO UserVotes (user_id, event_id, chosen_winner_id)
                        VALUES (?, ?, (SELECT team_id FROM Teams WHERE team_name = ? AND sport = ?));
                    """, (user_id, event_id, chosen_winner, sport_type))
                    con.commit()
                    

        return leaderboard()

    return "User not found."


@app.route("/login")
def loginPage():
    return "login here"


@app.route("/test/<name>")
def testArgument(name=None):
    return "testing if the name works: " + str(name)
