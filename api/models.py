from db import get_connection
from secrets_code import create_code
from redis_code import set_code, get_code

def get_recipes(keyword: str, ingredients = None, difficulty = None, dish_type = None, diet_type = None, food_groups = None):
    db = get_connection()
    cur = db.cursor()
    try:
        query = """
            SELECT DISTINCT recipes.id, 
                                recipes.title, 
                                recipes.summary, 
                                recipes.cooking_time,
                                recipes.approx_price,
                                recipes.servings,
                                recipes.image,
                                recipes.license,
                                recipes.link
                                FROM recipes """
        joins = """ """ 
        wheres = """WHERE (LOWER(recipes.title) LIKE LOWER (?) OR LOWER(recipes.summary) LIKE LOWER(?) OR LOWER(recipes.instructions) LIKE LOWER(?)) """
        params = ["%" + keyword + "%", "%" + keyword + "%", "%" + keyword + "%"]
        
        if difficulty:
            joins += """JOIN difficulty ON recipes.difficulty_id = difficulty.id """
            wheres += """AND LOWER(difficulty.name) LIKE LOWER(?) """
            params.extend(["%" + difficulty +"%"])
        
        if dish_type:
            joins += """JOIN dish_type ON recipes.dish_type_id = dish_type.id """
            wheres += """AND LOWER(dish_type.name) LIKE LOWER(?) """
            params.extend(["%"+ dish_type +"%"])
        
        if ingredients or diet_type or food_groups:
            groups = """GROUP BY recipes.id """
            counts = """HAVING """
            if ingredients:   
                ing_sums = len(ingredients)
                placeholders = ' '.join(["OR LOWER(ingredients.name) LIKE LOWER(?)"] * (len(ingredients)-1))
                joins += """JOIN recipes_ingredients ON recipes.id = recipes_ingredients.recipes_id 
                            JOIN ingredients ON recipes_ingredients.ingredients_id = ingredients.id """ 
                wheres += f"""AND (LOWER(ingredients.name) LIKE LOWER(?) {placeholders}) """

                for ingredient in ingredients:
                    params.extend(["%" + ingredient + "%"])
                counts += """COUNT (DISTINCT ingredients.name) = ? """

            if diet_type:
                dt_sums = len(diet_type)
                placeholders = ' '.join(["OR LOWER(diet_type.name) LIKE LOWER(?)"]*(len(diet_type)-1))
                wheres += f"""AND (LOWER(diet_type.name) LIKE LOWER (?) {placeholders}) """
                joins += """JOIN recipes_diet_type ON recipes.id = recipes_diet_type.recipes_id
                            JOIN diet_type ON recipes_diet_type.diet_type_id = diet_type.id """
                for dt in diet_type:
                    params.extend(["%" + dt + "%"])
                if ingredients:
                    counts += """ AND COUNT (DISTINCT diet_type.name) = ? """
                else:
                    counts += """ COUNT (DISTINCT diet_type.name) = ? """
            if food_groups:
                fg_sums = len(food_groups)
                placeholders = ' '.join(["OR LOWER(food_groups.name) LIKE LOWER (?)"]*(len(food_groups)-1))
                wheres += f"""AND (LOWER(food_groups.name) LIKE LOWER (?){placeholders}) """
                joins += """JOIN recipes_food_groups ON recipes.id = recipes_food_groups.recipes_id
                            JOIN  food_groups ON recipes_food_groups.food_groups_id = food_groups.id """
                for fg in food_groups:
                    params.extend(["%" + fg + "%"])
                if ingredients or diet_type:
                    counts += """ AND COUNT (DISTINCT food_groups.name) = ? """
                else:
                    counts += """ COUNT (DISTINCT food_groups.name) = ? """


            if ingredients:
                params.append(ing_sums)
            if diet_type:
                params.append(dt_sums)
            if food_groups:
                params.append(fg_sums)

            recipes = cur.execute(query + joins + wheres + groups + counts + ";", params)

        else: 

            recipes = cur.execute(query + joins + wheres + ";", params )
        
        recipes = recipes.fetchall()
        

    except Exception as e:
        
        return {"error": e}
    
    finally:
        db.close()

    return recipes

def get_id(recipe_id:int):
    db = get_connection()
    cur = db.cursor()
    try:
        recipes_query = f"""SELECT recipes.id,
                            recipes.title,
                            recipes.cooking_time,
                            recipes.approx_price,
                            recipes.servings,
                            recipes.instructions,
                            recipes.link, 
                            recipes.license,
                            recipes.image,
                            dish_type.id,
                            dish_type.name
                                   
                    from recipes
                    JOIN dish_type ON recipes.dish_type_id = dish_type.id
                    WHERE recipes.id = {recipe_id}
                    GROUP BY recipes.id;
       """
        recipes_query = cur.execute(recipes_query)
        recipes_response = recipes_query.fetchall()

        ingredients_query = f"""SELECT ingredients.id, ingredients.name, recipes_ingredients.quantity, measure_type.name from ingredients 
                    JOIN recipes_ingredients ON ingredients.id = recipes_ingredients.ingredients_id 
                    JOIN recipes ON recipes_ingredients.recipes_id = recipes.id
                    JOIN measure_type ON recipes_ingredients.measure_type_id = measure_type.id
                    WHERE recipes.id = {recipe_id}
                    """                
        ingredients_query = cur.execute(ingredients_query)
        ingredients_response = ingredients_query.fetchall()

        diet_type_query = f"""SELECT diet_type.id, diet_type.name from diet_type
                    JOIN recipes_diet_type ON diet_type.id = recipes_diet_type.diet_type_id
                    JOIN recipes ON recipes_diet_type.recipes_id = recipes.id
                    WHERE recipes.id = {recipe_id}
                    """
        diet_type_query = cur.execute(diet_type_query)
        diet_type_respose = diet_type_query.fetchall()

        food_groups_query = f"""SELECT food_groups.id, food_groups.name from food_groups
                    JOIN recipes_food_groups ON food_groups.id = recipes_food_groups.food_groups_id
                    JOIN recipes ON recipes_food_groups.recipes_id = recipes.id
                    WHERE recipes.id = {recipe_id}"""
        
        food_groups_query = cur.execute(food_groups_query)
        food_groups_response = food_groups_query.fetchall()
        
        return recipes_response, ingredients_response, diet_type_respose, food_groups_response
    except Exception as e:
        return {"error:", e}
    finally:
        db.close()

def create_recipe(create_r):
  db = get_connection()
  cur = db.cursor()

  title = create_r["title"]
  summary = create_r["summary"]
  cooking_time = create_r["cooking_time"]
  approx_price = create_r["approx_price"]
  servings = create_r["servings"]
  instructions = create_r["instructions"]
  link = create_r["link"]
  license = create_r["license"]
  image = create_r["image"]
  email = create_r["email"]
  difficulty = create_r["difficulty"]
  dish_type = create_r["dish_type"]
  food_groups = create_r["food_groups"]
  ingredients =  create_r["ingredients"]
  diet_type = create_r["diet_type"]

  try:
    #Getting the difficulty_id and dish_type_id to insert into the recipe table
    cur.execute("""SELECT id FROM difficulty WHERE name = ?;""", (difficulty.capitalize(), ))
    difficulty_id = cur.fetchone()[0]
    cur.execute("""SELECT id FROM dish_type WHERE name = ?;""", (dish_type.capitalize(), ))
    dish_type_id = cur.fetchone()[0]

  

   #Inserting all the data into the recipe table.
    cur.execute("INSERT OR IGNORE INTO recipes (title, summary, cooking_time, approx_price, servings, instructions, difficulty_id, dish_type_id, link, license,image, email) VALUES (?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(title) DO NOTHING",(title, summary, cooking_time, approx_price, servings, instructions, difficulty_id, dish_type_id, link, license, image, email))
    cur.execute("SELECT id FROM recipes where title = (?)", (title, ))
    recipe_id = cur.fetchone()[0]

    #Inserting the measure types, ingredients, quantities, diet_types and food_groups and retrieving the corresponding IDs
    for r in ingredients:
      cur.execute("""INSERT OR IGNORE INTO measure_type (name) VALUES (?) ON CONFLICT DO NOTHING;""", (r[1].capitalize(), ))
      cur.execute("SELECT id FROM measure_type where name = (?)", (r[1].capitalize(),))
      measure_type_id = cur.fetchone()[0]
      cur.execute("INSERT INTO ingredients (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (r[2].capitalize(),))
      cur.execute("SELECT id FROM ingredients where name = (?)", (r[2].capitalize(),))
      ingredients_id = cur.fetchone()[0]
      #inserting information in the recipes_ingredients table
      cur.execute("INSERT OR IGNORE INTO recipes_ingredients (recipes_id, ingredients_id, measure_type_id, quantity) VALUES (?, ?, ?, ?)", (recipe_id, ingredients_id, measure_type_id, r[0]))
    
    for dt in diet_type:
      cur.execute("INSERT OR IGNORE INTO diet_type (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (dt.capitalize(),))
      cur.execute("SELECT id FROM diet_type where name = (?)", (dt.capitalize(),))
      diet_type_id = cur.fetchone()[0]
      cur.execute("INSERT OR IGNORE INTO recipes_diet_type (recipes_id, diet_type_id) VALUES (?, ?)", (recipe_id, diet_type_id))

    for fg in food_groups:
      cur.execute("INSERT OR IGNORE INTO food_groups (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (fg.capitalize(),))
      cur.execute("SELECT id FROM food_groups where name = (?)", (fg.capitalize(),))
      food_groups_id = cur.fetchone()[0]
      cur.execute("INSERT OR IGNORE INTO recipes_food_groups (recipes_id, food_groups_id) VALUES (?, ?)", (recipe_id, food_groups_id))
      
    db.commit()
    return {"message": f"The recipe {title} has been successfully added"}

  except Exception as e:
    db.rollback()
    return {"error": "The recipe has not been created beacuse:"}, e

  finally:
    db.close()

def user_verif(user_details: dict):

    db = get_connection()
    cur = db.cursor()
    try:
        recipe_id = user_details["id"]
        user_email = user_details["email"]

        recipe_details = cur.execute("""SELECT id, email FROM recipes WHERE id = ?; """, (recipe_id, ))
        recipe_details = recipe_details.fetchall()
        if recipe_id != recipe_details[0][0] or user_email != recipe_details[0][1]:
            return {"status": False, "message": "The provided user details do not correspond to the recipe information.Verify your information to be identified as a user."} 
        else:    
            code = create_code()
            set_code(recipe_id, code)
            return {"status": True, "message": code}
    
    except Exception as e:
        db.rollback()
        return {"error": e}

    finally:
        db.close()

def update_recipe(updates:dict):
    db = get_connection()
    cur = db.cursor()
    code = updates['code']
    id = updates['id']
    title = updates["title"]
    summary = updates["summary"]
    cooking_time = updates["cooking_time"]
    approx_price = updates["approx_price"]
    servings = updates["servings"]
    instructions = updates["instructions"]
    link = updates["link"]
    license = updates["license"]
    image = updates["image"]
    email = updates["email"]
    difficulty = updates["difficulty"]
    dish_type = updates["dish_type"]
    food_groups = updates["food_groups"]
    ingredients =  updates["ingredients"]
    diet_type = updates["diet_type"]
    
   

    response = get_code(code)
    recipe_details = cur.execute("""SELECT id, email FROM recipes WHERE id = ?;""", (id, ))
    recipe_details = recipe_details.fetchall()
   
    if response == code and recipe_details[0][0] == id and recipe_details[0][1] == email:
        try:
            
            cur.execute("""SELECT id FROM difficulty WHERE name = ?;""", (difficulty.capitalize(), ))
            difficulty_id = cur.fetchone()[0]
            
            cur.execute("""SELECT id FROM dish_type WHERE name = ?;""", (dish_type.capitalize(), ))
            dish_type_id = cur.fetchone()[0]
    
            cur.execute("""UPDATE recipes SET title = ?, summary = ?, cooking_time = ?, approx_price = ?, servings = ?, image = ?, instructions = ?, license = ?, link= ?, difficulty_id = ?, dish_type_id = ? WHERE id = ?;""",(title, summary, cooking_time, approx_price, servings, image, instructions, license, link, difficulty_id, dish_type_id, id))
           
            cur.execute("""DELETE FROM recipes_ingredients where recipes_id = ?; """, (id,))
            cur.execute("""DELETE FROM recipes_diet_type where recipes_id = ?; """, (id,))
            cur.execute("""DELETE FROM recipes_food_groups where recipes_id = ?; """, (id,))
            for r in ingredients:
                cur.execute("""INSERT OR IGNORE INTO measure_type (name) VALUES (?) ON CONFLICT DO NOTHING;""", (r[1].capitalize(), ))
                cur.execute("SELECT id FROM measure_type where name = (?)", (r[1].capitalize(),))
                measure_type_id = cur.fetchone()[0]
                cur.execute("INSERT INTO ingredients (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (r[2].capitalize(),))
                cur.execute("SELECT id FROM ingredients where name = (?)", (r[2].capitalize(),))
                ingredients_id = cur.fetchone()[0]
                #inserting information in the recipes_ingredients table
                cur.execute("INSERT OR IGNORE INTO recipes_ingredients (recipes_id, ingredients_id, measure_type_id, quantity) VALUES (?, ?, ?, ?)", (id, ingredients_id, measure_type_id, r[0]))
            
            for dt in diet_type:
                cur.execute("INSERT OR IGNORE INTO diet_type (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (dt.capitalize(),))
                cur.execute("SELECT id FROM diet_type where name = (?)", (dt.capitalize(),))
                diet_type_id = cur.fetchone()[0]
                cur.execute("INSERT OR IGNORE INTO recipes_diet_type (recipes_id, diet_type_id) VALUES (?, ?)", (id, diet_type_id))

            for fg in food_groups:
                cur.execute("INSERT OR IGNORE INTO food_groups (name) VALUES (?) ON CONFLICT(name) DO NOTHING", (fg.capitalize(),))
                cur.execute("SELECT id FROM food_groups where name = (?)", (fg.capitalize(),))
                food_groups_id = cur.fetchone()[0]
                cur.execute("INSERT OR IGNORE INTO recipes_food_groups (recipes_id, food_groups_id) VALUES (?, ?)", (id, food_groups_id))
        
            db.commit()
            return {"message": "The recipes has been successfully updated"}, 200
        
        except Exception as e:
            db.rollback()
            return {"error": "There was an error updating the recipe", "details": str(e)}, 500

        finally:
            db.close()

    else:
        return{"message":"The details you provided do not match our records. Please double-check and try again"}, 401
    


