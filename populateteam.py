import sqlite3
import random

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

# Function to generate team logo URL
def generate_logo_url(team_name, sport_type):
    return ""

# Connect to the SQLite database
conn = sqlite3.connect("database.db")
cursor = conn.cursor()

# Create Teams table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS Teams (
        team_id INTEGER PRIMARY KEY,
        team_name TEXT,
        team_location TEXT,
        team_logo_url TEXT,
        sport TEXT
    )
''')

# Populate the Teams table with dummy data
team_id = 1
for team_name in team_names:
    for sport_type in sport_types:
        team_location = team_name
        team_logo_url = generate_logo_url(team_name, sport_type)

        # Insert data into the table
        cursor.execute('''
            INSERT INTO Teams
            (team_id, team_name, team_location, team_logo_url, sport)
            VALUES (?, ?, ?, ?, ?)
        ''', (team_id, team_name, team_location, team_logo_url, sport_type))
        
        # Increment team ID for each entry
        team_id += 1

# Commit the changes
conn.commit()

# Close the connection
conn.close()

print("Teams table populated with dummy data.")
