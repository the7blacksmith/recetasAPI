
# recetasAPI 🥘
**Recipes API: API for managing Spanish recipes with filters and ingredient details.**

## Technologies Used

- **Python**: The main programming language used.
- **Flask**: The framework used to build the  API.
- **SQLite3**: The database used to store recipe data in a lightweight, serverless format.
- **Git**: Version control system used for managing code and collaboration.
- **Virtualenv** (if used): Tool to create isolated Python environments.

## The database
The database started with the following relational diagram:

![Entity-Relationship Diagram](database/images/Entity-Relationship%20Diagram.png)

Although I plan to make some amendments in the future to address emerging needs, this diagram represents the foundation of my project. The database is organized into multiple tables, with the Recipes table as the main one, containing essential information about each recipe.

In addition to the Recipes table, the database includes the following tables to provide comprehensive and detailed information:

- Ingredients table: Stores the ingredients used in each recipe.
- Diet Type table: Specifies dietary categories 
- Food Group table: Classifies ingredients into nutritional groups.
- Difficulty table:  The level of complexity required to prepare each recipe.
- Dish Type table: Based on the type of dish.

These additional tables are related to the Recipes table, allowing for a well-organized and easily expandable structure that enhances the flexibility of the application.

There are also two files in the database folder.

1. **script.py** -\> this script is responsible for creating the database along with all the necessary tables.
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
This makes it easy to explore and interact with the API without having to manually add data.
  
**Quick Start**

To quickly set up the database and load the initial recipes, execute the following commands:

python3 script.py

python3 seeds.py

