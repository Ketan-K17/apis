from flask import Flask, jsonify, request
from http import HTTPStatus

app = Flask(__name__)

# some memory to store initially.
recipes = [
    {
        'id': 1,
        'name': 'Egg Salad',
        'description': 'This is a lovely egg salad recipe.'
    },
    {
        'id': 2, 'name': 'Tomato Pasta',
        'description': 'This is a lovely tomato pasta recipe.'
    }
]

# get ALL recipes
@app.route("/recipes", methods = ['GET'])
def get_recipes():
    return jsonify({
        'data': recipes
    })

# get recipe by id
@app.route("/recipes/<int:recipe_id>", methods = ['GET'])
def get_recipes_by_id(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    if recipe:
        return jsonify({
            'data': recipe
        }), HTTPStatus.OK
    return jsonify({
        'message': 'Recipe not found'
    }), HTTPStatus.NOT_FOUND

# create recipe
@app.route("/recipes", methods = ['POST'])
def create_recipe():
    data = request.get_json()
    recipe = {
        'id': len(recipes) + 1,
        'name': data.get('name'),
        'description': data.get('description')
    }
    recipes.append(recipe)
    return jsonify(recipe), HTTPStatus.CREATED

# update recipe
@app.route("/recipes/<int:recipe_id>", methods = ['PUT'])
def update_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    if recipe:
        data = request.get_json()
        # this is a nice way to update an existing dictionary.
        recipe.update(
            {
                'name': data.get('name'),
                'description': data.get('description')
            }
        )
        return jsonify(recipe), HTTPStatus.OK
    return jsonify({
        'message': 'Recipe not found'
    }), HTTPStatus.NOT_FOUND

@app.route("/recipes/<int:recipe_id>", methods = ['DELETE'])
def delete_recipe(recipe_id):
    recipe = next((recipe for recipe in recipes if recipe['id'] == recipe_id), None)
    if recipe:
        recipes.remove(recipe)
        return jsonify({
            'message': 'Recipe deleted successfully'
        }), HTTPStatus.NO_CONTENT
    return jsonify({
        'message': 'Recipe not found'
    }), HTTPStatus.NOT_FOUND

if __name__ == "__main__":
    app.run()

