from marshmallow import Schema, fields

class RecipeSchema(Schema):
    title = fields.Str(required=True)
    summary = fields.Str(required=True)
    cooking_time = fields.Str(required=True)
    approx_price = fields.Float(required=True)
    servings = fields.Int(required=True)
    instructions = fields.Str(required=True)
    link = fields.Str(required=True)
    license = fields.Str(required=True)
    image = fields.Str(required=True)
    email = fields.Str(required=True)
    difficulty = fields.Str(required=True)
    dish_type = fields.Str(required=True)
    food_groups = fields.List(fields.Str(), required=True)
    ingredients = fields.List(fields.List(fields.Raw()), required=True)
    diet_type = fields.List(fields.Str(required=True))
    id = fields.Int(required=False)
    code = fields.Str(required=False)

recipe_schema = RecipeSchema()
