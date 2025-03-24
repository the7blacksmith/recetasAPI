from db import get_connection
from pprint import pprint


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
        print("ERROR:", e)
        return None
    
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
        print("ERROR:", e)
    finally:
        db.close()
    




