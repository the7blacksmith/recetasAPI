import sqlite3

def get_connection(database = "../database/recipes.db"):
    try:
        connection = sqlite3.connect(database)
        connection.execute("PRAGMA foreign_keys = ON")
        return connection
    except Exception as e:
        print("ERROR: Unable to connect to the database:", e)
        return None

