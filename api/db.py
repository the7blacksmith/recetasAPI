import sqlite3

def get_connection(database = "../database/recipes.db"):
    try:
        connection = sqlite3.connect(database)
        return connection
    except Exception as e:
        print("ERROR: Unable to connect to the database:", e)
        return None

# if __name__ == "__main__":
#     db_connection = get_connection() #Llamo a la clase.
#     if db_connection:
#         cur = db_connection.cursor() #llamo al método de la clase.  
#         dificultad = cur.execute("Select * from difficulty;")
#         dif = cur.fetchall()
#         print(dif)
#         db_connection.close()
