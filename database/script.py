import sqlite3

conn = sqlite3.connect("recipes.db")
cur = conn.cursor()

cur.executescript('''
    DROP TABLE IF EXISTS recipes;
    DROP TABLE IF EXISTS ingredients;
    DROP TABLE IF EXISTS diet_type;
    DROP TABLE IF EXISTS difficulty;
    DROP TABLE IF EXISTS dish_type;
    DROP TABLE IF EXISTS recipes_ingredients;
    DROP TABLE IF EXISTS recipes_diet_type;
    DROP TABLE IF EXISTS measure_type;
    DROP TABLE IF EXISTS food_groups;
    DROP TABLE IF EXISTS recipes_food_groups;

                  
    CREATE TABLE recipes(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        title TEXT NOT NULL UNIQUE,
        summary TEXT NOT NULL,
        cooking_time TEXT,
        approx_price REAL,
        servings INTEGER,
        instructions TEXT,
        difficulty_id INTEGER,
        dish_type_id INTEGER,
        link TEXT,
        license TEXT,
        image TEXT,
        email TEXT NOT NULL,
        FOREIGN KEY (difficulty_id) REFERENCES difficulty(id) ON DELETE SET NULL,
        FOREIGN KEY (dish_type_id) REFERENCES dish_type(id) ON DELETE SET NULL
    );

    CREATE TABLE ingredients(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL              
    );
                  
    CREATE TABLE diet_type(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );

    CREATE TABLE difficulty(
        id INTEGER PRIMARY KEY,
        name TEXT UNIQUE NOT NULL
    );
                  
    CREATE TABLE dish_type(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
                  
    CREATE TABLE recipes_ingredients(
    recipes_id INTEGER,
    ingredients_id INTEGER,
    measure_type_id INTEGER,
    quantity REAL,
    PRIMARY KEY (recipes_id, ingredients_id, measure_type_id),
    FOREIGN KEY (recipes_id) REFERENCES recipes(id) ON DELETE CASCADE,
    FOREIGN KEY (ingredients_id) REFERENCES ingredients(id) ON DELETE RESTRICT,
    FOREIGN KEY (measure_type_id) REFERENCES measure_type(id) ON DELETE SET NULL
);
                  
    CREATE TABLE recipes_diet_type(
        recipes_id INTEGER,
        diet_type_id INTEGER,
        FOREIGN KEY (recipes_id) REFERENCES recipes(id) ON DELETE CASCADE,
        FOREIGN KEY (diet_type_id) REFERENCES diet_type(id) ON DELETE RESTRICT,
        PRIMARY KEY (recipes_id, diet_type_id)
    );

    CREATE TABLE measure_type(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );

    
    CREATE TABLE food_groups(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL
    );
                  
    CREATE TABLE recipes_food_groups(
        recipes_id INTEGER,
        food_groups_id INTEGER,
        FOREIGN KEY (recipes_id) REFERENCES recipes(id) ON DELETE CASCADE,
        FOREIGN KEY (food_groups_id) REFERENCES food_groups(id) ON DELETE RESTRICT,
        PRIMARY KEY (recipes_id, food_groups_id)
    )
''')

conn.commit()
conn.close()

