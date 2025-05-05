
# recetasAPI 🥘
**Recipes API: API for managing Spanish recipes with filters and ingredient details.**

## Technologies Used

- **Python**
- **Flask**
- **SQLite3**
- **Git**
- **Virtualenv**
- **Marshmallow and flask-marshmallow**

## The database
The database started with the following relational diagram:

![Entity-Relationship Diagram][image-1]

Although I plan to make some amendments in the future to address emerging needs, this diagram represents the foundation of my project. The database is organized into multiple tables, with the Recipes table as the main one, containing essential information about each recipe.

In addition to the Recipes table, the database includes the following tables to provide comprehensive and detailed information:

- Ingredients table: Stores the ingredients used in each recipe.
- Diet Type table: Specifies dietary categories 
- Food Group table: Classifies ingredients into nutritional groups.
- Difficulty table:  The level of complexity required to prepare each recipe.
- Dish Type table: Based on the type of dish.

These additional tables are related to the Recipes table, allowing for a well-organized and easily expandable structure that enhances the flexibility of the application.

There are also two files in the database folder.

1. **script.py** -\> this script is responsible for creating the database and all the necessary tables.
When executed, it will generate the following tables:

- recipes
- recipes\_ingredients
- ingredients
- measure\_type
- recipes\_diet\_type
- diet\_type
- recipes\_food\_groups
- food\_groups
- difficulty                 
- dish\_type

2. **seeds.py** -\> this script is used to populate the database with initial data to test and experiment with the API.
It will add 19 classic Spanish recipes along with their ingredients and complementary information in the related tables.
This makes it easy to explore and interact with the API without manually adding data.
  
**Quick Start**

To quickly set up the database and load the initial recipes, execute the following commands:

- python3 script.py
- python3 seeds.py

## The API

This API allows you to manage and search for recipes stored in the database, offering flexible filtering options to get precise results based on your criteria. At the moment, it has two main endpoints:
1.   General recipe search: Retrieves a list of recipes that match the specified filters.
2.   Recipe details: Shows detailed information about a specific recipe using its ID.

The API is built with Flask, following best practices for project structure, and SQLite3 for data management. It is designed to adhere to RESTful API principles as much as possible, ensuring clear and consistent endpoint naming, proper use of HTTP methods, and stateless interactions. This not only makes the API intuitive and easy to use but also aligns with modern standards for maintainability and scalability.

**Project Structure**
- main.py: The entry point that starts and manages the Flask server.
- db.py: This handles the connection to the SQLite database, and it can be imported in the other .py files.
- models/: Contains Python functions that interact directly with the database.
- routes/: Defines the API endpoints and processes incoming requests by interacting with models.py to fetch the needed data.

## How to Use the API

## 1. Searching for Recipes

**GET http://localhost:port/recipes**

This endpoint lets you search for recipes stored in the database using a variety of filters. The **keyword** filter is required, while the others are optional and can be combined as needed.

Available Filters

- **keyword** (*required*): Filters recipes containing the specified text in the title, summary, or instructions.
  
	Example:

		- http://localhost:port/recipes?keyword=tortilla
  
- **ingredients** (*optional*): Filters recipes that include one or more specified ingredients.
  
	Example:

		- http://localhost:port/recipes?keyword=tortilla&ingredients=cebolla
  
		- http://localhost:port/recipes?keyword=tortilla&ingredients=huevo&ingredients=patatas

- **diet_type** (*optional*): Filters recipes according to dietary preferences, which can be combined with other filters.

  	Example:
  
  		- http://localhost:port/recipes?keyword=tortilla&diet_type=vegetariana
  
  		- http://localhost:port/recipes?keyword=pasta&diet_type=sin+lactosa&diet_type=vegana
  
- **food_groups** (*optional*): Filters by food groups, like “carne”, "Verduras", or “Pasteles”. You can specify more than one.

  	Example:
  
  		- http://localhost:port/recipeskeyword=tortilla&food_groups=carne&food_groups=patatas
  
  		- http://localhost:port/recipes?keyword=tortilla&diet_type=vegetariana&food_groups=tapas+calientes
  
- **difficulty** (*optional*, **single-use**): Filters recipes by difficulty level ("fácil", "medio", "difícil", "profesional”).

  	Example:
  
		- http://localhost:port/recipes?keyword=tomate&difficulty=medio
  
- **dish_type** (*optional*, **single-use**): Specifies the type of dish, like "starter", "main course", or "dessert".

  	Example:
  
		- http://localhost:port/recipes?keyword=tomate&dish_type=primer+plato  
	  


#### Example Response (Search)

This is an example of the JSON response you can get by filtering, as shown above.

![recipes_search](database/images/recipes_search.png)


## 2. Searching for an accurate recipe:
   
**GET http://localhost:port/recipes/{id}**

This endpoint returns detailed information about a specific recipe, identified by its ID.

#### Usage Examples

http://localhost:port/recipes/id/4

http://localhost:port/recipes/id/18

#### Example Response

This is an example of the JSON response you can get by filtering, as shown above.

![recipes_search](database/images/id_search.png)

Below are the filters you can use in your searches using the API

**ingredients**

- Harina
- Azúcar
- Sal
- Huevos
- Leche
- Mantequilla
- Aceite de oliva
- Levadura
- Vainilla
- Chocolate
- Fresas
- Manzanas
- Zanahorias
- Papas
- Cebollas
- Tomates
- Pollo
- Carne molida
- Queso
- Orégano
- Pimienta
- Canela
- Albahaca
- Ajo
- Limón
- Arroz
- Frijoles
- Pan
- Crema
- Champiñones
- Espinacas
- Perejil
- Chile
- Apio
- Pimientos
- Miel
- Jengibre
- Cilantro
- Mostaza
- Ketchup
- Salsa de soya
- Vinagre
- Caldo de pollo
- Pescado
- Camarones
- Lentejas
- Yogur
- Almendras
- Nueces
- Pasas
- Maíz
- Avena
- Pan integral
- Aguacate

**diet_type**

- Vegetariana
- Vegana
- Sin gluten
- Sin lactosa
- Sin trigo
- Baja en carbohidratos
- Keto (Cetogénica)
- Mediterránea
- Dieta DASH
- Dieta nórdica
- Sin azúcar
- Baja en sodio
- Alta en proteínas
- Baja en grasas
- Dieta macrobiótica
- Dieta carnívora
- Sin soja
- Sin huevo
- Low FODMAP
- Whole30
- Dieta baja en colesterol
- Dieta rica en fibra
- Dieta hiperprotéica
- Dieta para diabéticos
- Dieta DASH vegetariana
- Dieta rica en calcio
- Dieta sin cítricos
- Dieta sin fructosa

**difficulty**

- Fácil
- Medio
- Difícil
- Profesional

**dish_type**

- Entrante
- Plato principal
- Acompañamientos
- Postre
- Bebida

**food_groups**

- Tapas Calientes
- Tapas frías
- Canapé
- Hojaldres
- Empanadillas
- Empanadas
- Crudités
- Carpaccio
- Salsas
- Encurtidos
- Carnes
- Aves
- Ensaladas
- Verduras
- Purés
- Patatas
- Panes
- Hojaldres
- Pescados
- Tartas
- Pasteles
- Helados
- Sorbetes
- Flanes y puddings
- Galletas
- Bizcochos
- Frutas
- Soufflés
- Mariscos
- Cócteles
- Bebidas refrescantes
- Batidos y licuados
- Pasta
- Arroces
- Guisos y potajes
- Parrilla o Barbacoa
- Platos al horno
- Frituras
- Platos étnicos

## 3. Create a New Recipe

**POST http://localhost:port/recipes**

This endpoint allows users to add a new recipe to the database by sending a properly structured JSON object via a POST request. All fields are mandatory, and the request must include all necessary information in the specified format.

To send a POST request with JSON data, you can use a variety of tools, such as **Thunder Client** (VS Code extension), **Postman**, or any other that suits you.

The API uses **Marshmallow** for data validation. If any required field is missing or improperly formatted, the request will fail, and the server will return an error message indicating which field is problematic.

#### Field List & Data Types

All of the following fields are required and must be included in your POST request:

- title: string -> The name of the recipe. It must be unique.
- summary: string -> A short description of the recipe.
- instructions: string -> Step-by-step instructions for preparing the recipe.
- difficulty: string -> Difficulty level. Must match an existing entry in the difficulty table (e.g., "Easy").
- dish_type: string -> Type of dish. Must match an entry in the dish_type table (e.g., "Main Course").
- diet_type: array of strings -> A list of associated diet types. (e.g., ["Vegetarian"]).
- food_groups: array of strings -> A list of related food groups. (e.g., ["Meats"]).
- ingredients: array of objects -> A list of ingredients used in the recipe. Each ingredient object must include the following:
	1. name: string -> Ingredient name (e.g., "eggs").
	2. quantity: integer -> Quantity used in the recipe (e.g., 4).
	3. measure_type: string -> Unit of measurement (e.g., "grams", "teaspoon").

- cooking_time: string -> The time required to cook the recipe in minutes (e.g., "15").
- approx_price: float -> Approximate cost of the recipe (e.g., 5.0).
- servings: integer -> Number of servings the recipe makes (e.g., 4).
- link: string -> A URL link associated with the recipe (e.g., "www.create_recetitas.com").
- license: string -> License information (e.g., "ChatGPT").
- image: string -> A URL or path to an image representing the recipe (e.g., "images/pancakes.png").
- email: string -> Contact email for recipe authorship (e.g., "noemail@email.com").

You can see below an example of a JSON you can use to create a new recipe in the database.

{"title": "Tortitas",
  "summary": "Deliciosos y esponjosos pancakes, ideales para un desayuno reconfortante. Se sirven con miel, frutas o sirope para un toque extra de sabor.",
  "cooking_time": "15",
  "approx_price": 5.0,
  "servings": 4,
  "instructions": "'1. En un bol grande, mezclar la harina, el azúcar, el polvo de hornear y la sal.\n' '2. En otro bol, batir el huevo, añadir la leche y la mantequilla derretida.\n' '3. Agregar los ingredientes líquidos a los ingredientes secos y mezclar hasta obtener una masa suave.\n''4. Calentar una sartén antiadherente a fuego medio-alto y engrasarla con un poco de mantequilla.\n''5. Verter 1/4 de taza de la masa en la sartén caliente y cocinar durante 2-3 minutos por cada lado o hasta que estén dorados.\n''6. Servir calientes con tus acompañamientos favoritos como frutas, miel o sirope de arce.'",
  "difficulty": "Fácil",
  "dish_type": "Postre",
  "food_groups": ["Harinas", "Lácteos", "Desayunos"],
  "ingredients": [
    [1, "Taza", "Harina de trigo"],
    [2, "Cucharadas", "Azúcar"],
    [2, "Cucharaditas", "Polvo de hornear"],
    [1, "Pizca", "Sal"],
    [1, "Unidad", "Huevo"],
    [1, "Taza", "Leche"],
    [2, "Cucharadas", "Mantequilla derretida"],
    [1, "Cucharada", "Mantequilla"]
  ],
  "diet_type": ["vegetariana"],
  "link": "www.create_recetitas.com",
  "license": "ChatGPT",
  "image": "images/pancakes.png",
  "email": "xxxx@email.com"
}

### Error Handling

During recipe creation, the following errors may occur:

- 400 Bad Request: No data was provided in the request body.

- 422 Unprocessable Entity: The submitted data did not pass validation (e.g., missing required fields, incorrect data types, or invalid values).
Message: A detailed error message will be returned indicating which fields are invalid.

- 500 Internal Server Error: An unexpected error occurred while attempting to insert the recipe into the database. If available, a "details" field may also be included with additional technical context.

- 201 Created: The recipe was successfully added to the database.


## 4. Verification

### Endpoint for verification before recipe modification or deletion.

The API includes a lightweight verification system to ensure secure modifications or deletions of recipes. This system sends a temporary code to the email associated with the recipe, which the user must use to proceed with any changes. This adds a layer of security without requiring full user authentication.

### How It Works
  
**POST http://localhost:port/recipes/recipes/verification**

- Request Body

You must provide the recipe ID and the email address used when the recipe was created. This data must be sent in JSON format:

{"id": 1, "email": "address@email.com"}

You can check the recipe ID by following the steps in the 'Searching for Recipes' section.

This initiates the process of generating and sending a verification code to the specified email address.

- Validation Process
  
The system first checks that both the provided id and email match an existing recipe in the database.

- Code Generation
  
If the validation is successful, a secure verification code is created using Python’s **secrets** library. This ensures the code is cryptographically secure and random.

- Temporary Storage
  
The generated code is stored temporarily using **Redis**, and remains valid for 15 minutes. Redis must be installed and running for this feature to work properly.

- Email Delivery
  
The code is sent via email using **Flask-Mail**. This library must also be installed and properly configured. A success response will be returned once the email is sent.

### Error Handling
  
During the verification process, the following errors may occur:

- 500 Internal Server Error: An error occurred while attempting to send the verification code via email.

- 422 Unprocessable Entity: An unexpected error occurred while processing the request (e.g., missing fields, mail configuration issues).

- 200 OK: The verification code was successfully generated and sent to the provided email address.

## 5. Updating an Existing Recipe

**PUT http://localhost:port/recipes**

This endpoint allows users to update an existing recipe in the database. To ensure security, you must include a verification code (sent previously to your email via the verification process) along with the complete, updated recipe data. The recipe id would not be necessary as it has been included in the URL.

All fields must be included in the request's body, even if you are only updating a few of them. Think of it as overwriting the recipe with a new version.

You can use tools such as Thunder Client, Postman, or any other API client to send the PUT request with a properly structured JSON object.

### Requirements for Update

You must have completed the verification process and received a valid verification code.

- The code must still be active (valid for 15 minutes after generation).

- All fields must be included in the JSON request (even if unchanged).

- The structure must follow the same format as for recipe creation.

### Process Overview

The server verifies that:

The provided code matches the one stored for the associated recipe ID.

The code has not expired.

If verification is successful, the recipe is updated in the database.

A success message is returned confirming the update.

### Error Handling

During the recipe update, the following errors may occur:

- 401 Unauthorized: The provided details (ID, email, or verification code) do not match the recipe.
Message: "The details you provided do not match our records. Please double-check and try again."

- 500 Internal Server Error: An error occurred while updating the recipe in the database.
Message: "There was an error updating the recipe."
In case of a server error, a "details" field is also included with technical information.

## 6. Deleting a Recipe

**DELETE http://localhost:port/recipes/{id}**

This endpoint allows users to delete an existing recipe from the database. 

### Steps you should follow:

1. You must have requested a verification code using the /recipes/verification endpoint.

2. The verification code must still be valid (it expires 15 minutes after generation).

3. You must send a DELETE request with the id (recipe id) in the URL and a JSON object that includes:

- email: The email address used when the recipe was created.

- code: The verification code received via email.

### Example Request Body

**DELETE http://localhost:port/recipes/34
{
  "email": "email@domain.com",
  "code": "8d2f4a"
}**

### Error Handling

During the recipe deletion process, the following errors may occur:

- 401 Unauthorized: The provided details (ID, email, or verification code) do not match the recipe.
Message: "The details you provided do not match our records. Please double-check and try again."

- 500 Internal Server Error: An error occurred while deleting the recipe from the database.
Message: "There was an error deleting the recipe."
A "details" field will also be included with technical information for debugging purposes if a server error occurs.

- 200 OK: The recipe has been successfully deleted. However, related details such as ingredients, diet types, or food groups will remain in their respective tables. While all links between the deleted recipe and those items are removed, the items themselves are preserved to enrich the database for future use—for example, if an ingredient like "lemon" was introduced by this recipe, it will still exist in the ingredients table even after the recipe is deleted.

[image-1]:	database/images/Entity-Relationship%20Diagram.png
