import sqlite3
import random
from datetime import datetime, timedelta

# List of team names
team_names = [
    "Austin College",
    "Centenary College of Louisiana",
    "Colorado College",
    "University of Dallas",
    "University of St. Thomas",
    "Schreiner University",
    "Southwestern University",
    "Texas Lutheran University",
    "Trinity University",
    "McMurry University",
    "University of the Ozarks",
    "Concordia University Texas",
    "McMurry University",
    "University of the Ozarks"
]

# List of possible sport types
sport_types = ["Football", "Volleyball", "Basketball", "Baseball"]

# Function to generate a random date within a given range
def random_date(start_date, end_date):
    return start_date + timedelta(
        days=random.randint(0, (end_date - start_date).days),
        hours=random.randint(0, 23),
        minutes=random.randint(0, 59),
        seconds=random.randint(0, 59)
    )

# Connect to the SQLite database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create SportingEvents table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS SportingEvents (
        event_id INTEGER PRIMARY KEY,
        event_name TEXT,
        event_date DATE,
        event_location TEXT,
        home_team_id INTEGER,
        away_team_id INTEGER,
        sport_type TEXT
    )
''')

# Populate the table with dummy data
event_id = 1
for sport_type in sport_types:
    for home_team in team_names:
        # Ensure Trinity University is either the home or away team
        if home_team == "Trinity University":
            away_team = random.choice([team for team in team_names if team != home_team])
        else:
            away_team = "Trinity University"

        # Query the Teams table for home team ID
        cursor.execute('''
            SELECT team_id
            FROM Teams
            WHERE team_name = ? AND sport = ?
        ''', (home_team, sport_type))
        home_team_id = cursor.fetchone()[0]

        # Query the Teams table for away team ID
        cursor.execute('''
            SELECT team_id
            FROM Teams
            WHERE team_name = ? AND sport = ?
        ''', (away_team, sport_type))
        away_team_id = cursor.fetchone()[0]

        # Generate data for the event
        event_name = f"{home_team} vs {away_team} - {sport_type}"
        event_date = random_date(datetime(2023, 1, 1), datetime(2023, 12, 31))
        event_location = home_team

        # Insert data into the table
        cursor.execute('''
            INSERT INTO SportingEvents
            (event_id, event_name, event_date, event_location, home_team_id, away_team_id, sport_type)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (event_id, event_name, event_date, event_location, home_team_id, away_team_id, sport_type))

        # Increment event ID for each entry
        event_id += 1

# Commit the changes and close the connection
conn.commit()
conn.close()

print("Database populated with dummy data.")
