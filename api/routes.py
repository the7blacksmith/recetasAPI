from flask import Blueprint, jsonify, request
from models import get_recipes, get_id, create_recipe, user_verif, update_recipe
from schemas import recipe_schema
from marshmallow import ValidationError
from send_code import s_code



recipes = Blueprint('recipes', __name__, url_prefix='/recipes')


@recipes.route("/", methods = ['GET'])
def search_recipes():
        keyword = request.args.get('keyword')
        ingredients = request.args.getlist('ingredients')
        difficulty = request.args.get('difficulty')
        dish_type = request.args.get('dish_type')
        food_groups = request.args.getlist('food_groups')
        diet_type = request.args.getlist('diet_type')

        if not keyword:
               return jsonify({"error": "Parameter 'keyword' is required"}), 400

        try:
                res = get_recipes(keyword, difficulty = difficulty, dish_type = dish_type, ingredients = ingredients, food_groups = food_groups, diet_type = diet_type)
                lista = []
                for id, title, summary, cooking_time, approx_price, servings, image, license, link in res:
                        diccionario = {"id": id, 
                                       "title": title, 
                                       "summary": summary, 
                                       "cooking_time": cooking_time, 
                                       "approx_price": approx_price, 
                                       "servings": servings, 
                                       "image": image, 
                                       "license": license, 
                                       "link": link}
                        lista.append(diccionario)
                if len(lista) > 0:
                       return jsonify(lista)
                else:
                       return jsonify({"error": "No recipes found matching the search criteria"}), 404
                
        except Exception as e:
            
            return jsonify({"error": e}), 500
        
@recipes.route('/<int:recipe_id>', methods = ['GET'])
def get_recipe_id(recipe_id):


        try:  
                recipe = get_id(recipe_id)
                
               
               

                if len(recipe[0])<1:
                        return jsonify({"error": "No recipe found with the given ID"}), 404
                
                else:
                        ing_list= []
                        for ing in recipe[1]:
                                ing_dict = {}
                                ing_dict["id"]=ing[0]
                                ing_dict["name"] = ing[1]
                                ing_dict["quantity"]= ing[2]
                                ing_dict["measure_type"]=ing[3]
                                ing_list.append(ing_dict)
                        dt_list = []
                        for dt in recipe[2]:
                                dt_dict= {}
                                dt_dict["id"] = dt[0]
                                dt_dict["name"]= dt[1]
                                dt_list.append(dt_dict)
                        
                        fg_list = []
                        for fg in recipe[3]:
                                fg_dict = {}
                                fg_dict["id"]=fg[0]
                                fg_dict["name"]=fg[1]
                                fg_list.append(fg_dict)

                        recipe_dict = {"id": recipe[0][0][0], 
                                "title": recipe[0][0][1], 
                                "cooking_time":recipe[0][0][2],
                                "aprox_price": recipe[0][0][3],
                                "servings": recipe[0][0][4],
                                "instructions": recipe[0][0][5],
                                "link": recipe[0][0][6],
                                "lincense": recipe[0][0][7],
                                "image": recipe[0][0][8],
                                "dish_type": {"id": recipe[0][0][9], 
                                "name":recipe[0][0][10]}, 
                                "ingredients" : ing_list,
                                "diet_type": dt_list,
                                "food_groups": fg_list
                                }

                        return recipe_dict, 200
        
        except Exception as e:
                
                return ({"error": e}), 500

@recipes.route('/', methods = ['POST'])
def new_recipe():
        recipe = request.get_json()
        if not recipe:
                return jsonify({"error": "No recipe data was provided."}), 400
        try: 
                recipe = recipe_schema.load(recipe)
                new_json_recipe = create_recipe(recipe)
                if "error" in new_json_recipe:
                        return jsonify(new_json_recipe), 500
                return jsonify({"message": "The recipe has been successfuly created"}), 201
        
        except ValidationError as e:
                return jsonify({"error": e.messages}), 422
@recipes.route('/verification', methods = ['POST'])
def verification():
        try:
                data = request.get_json()
                id = data["id"]
                email = data["email"]
                code = user_verif(data)

                if code["status"] == False:
                        return code["message"]
        
                else:
                        response, message = s_code(email, code["message"])
                        if response == True:
                                return jsonify({"success": True, "message": message}), 200
                        else:
                                return jsonify({"success": False, "message": message}), 500
                        
        except Exception as e:
                return jsonify ({"error": str(e)}), 422
        
@recipes.route('/', methods = ['PUT'])
def update():

        recipe_update = request.get_json()
        
        response = update_recipe(recipe_update)

        return response

@recipes.route('/<int:recipe_id>', methods=['DELETE'])
def delete(recipe_id):
        delete_details = request.get_json()
        id = recipe_id
        print(id)
        return delete_details

