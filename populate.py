import sqlite3
import random

# Connect to SQLite database (or create a new one if it doesn't exist)
conn = sqlite3.connect('database.db')
cursor = conn.cursor()

# Create UserVotes table if not exists
cursor.execute('''
    CREATE TABLE IF NOT EXISTS UserVotes (
        vote_id INTEGER PRIMARY KEY,
        user_id INTEGER,
        event_id INTEGER,
        chosen_winner_id INTEGER,
        FOREIGN KEY (user_id) REFERENCES Users(user_id),
        FOREIGN KEY (event_id) REFERENCES SportingEvents(event_id),
        FOREIGN KEY (chosen_winner_id) REFERENCES Teams(team_id)
    )
''')

# Fetch all game results with corresponding event_id
game_results = cursor.execute('SELECT event_id, winner_team_id FROM GameResults').fetchall()

# Fetch all users
users = cursor.execute('SELECT user_id FROM Users').fetchall()

# Populate UserVotes table with random votes for each game result and user
for user_id in range(1, 11):  # Assuming 10 users with user_ids 1-10
    for event_id, winner_team_id in game_results:
        # Fetch home_team_id and away_team_id from SportingEvents
        event_data = cursor.execute('SELECT home_team_id, away_team_id FROM SportingEvents WHERE event_id = ?', (event_id,)).fetchone()
        home_team_id, away_team_id = event_data

        # Randomly choose the chosen winner (either home_team_id or away_team_id)
        chosen_winner_id = home_team_id if random.choice([True, False]) else away_team_id

        cursor.execute('''
            INSERT INTO UserVotes (user_id, event_id, chosen_winner_id)
            VALUES (?, ?, ?)
        ''', (user_id, event_id, chosen_winner_id))

# Commit the changes and close the connection
conn.commit()
conn.close()

print("User votes have been generated and inserted into the UserVotes table.")
