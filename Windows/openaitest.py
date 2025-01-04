import sqlite3
from datetime import datetime

# Create a connection to the SQLite database
# If the file doesn't exist, it will be created
conn = sqlite3.connect('interaction_data.dll')

# Create a cursor object to execute SQL commands
cursor = conn.cursor()

# Create a table to store the interactions
cursor.execute('''
DELETE FROM interactions
''')

# Commit the changes and close the connection
conn.commit()
conn.close()
