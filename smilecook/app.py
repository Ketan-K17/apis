from flask import Flask
from flask_restful import Api
from resources.recipe import RecipeListResource, RecipeResource, RecipePublishResource

# initialize flask api 
app = Flask(__name__)
api = Api(app)

# add resource routing. All urls will now route to resources, and the resource defn will take care of the requests.
api.add_resource(RecipeListResource, '/recipes')
api.add_resource(RecipeResource, '/recipes/<int:recipe_id>')
api.add_resource(RecipePublishResource, '/recipes/<int:recipe_id>/publish')


if __name__ == '__main__':
    app.run(port=5000, debug=True)