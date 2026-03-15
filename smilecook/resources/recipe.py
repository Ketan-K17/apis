from flask import request
from flask_restful import Resource
from http import HTTPStatus
from models.recipe import Recipe, recipe_list


class RecipeListResource(Resource):
    # get all recipes
    def get(self):
        # init list of recipes to return
        data = []

        # add those recipes which have been published
        for recipe in recipe_list:
            if recipe.is_publish is True:
                data.append(recipe.data)
        return {"data": data}, HTTPStatus.OK

    def post(self):
        # unload data from request
        data = request.get_json()

        # wrap it as Recipe object
        recipe = Recipe(
            name=data["name"],
            description=data["description"],
            num_of_servings=data["num_of_servings"],
            cook_time=data["cook_time"],
            directions=data["directions"],
        )

        # append to list of recipes, since we're not adding it to db yet.
        recipe_list.append(recipe)

        # confirm that operation was successful
        return recipe.data, HTTPStatus.CREATED


class RecipeResource(Resource):
    # get a recipe
    def get(self, recipe_id):
        recipe = next(
            (
                recipe
                for recipe in recipe_list
                if recipe.id == recipe_id and recipe.is_publish == True
            ),
            None,
        )
        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND
        return recipe.data, HTTPStatus.OK

    # update a recipe
    def put(self, recipe_id):
        data = request.get_json()
        recipe = next(
            (
                recipe
                for recipe in recipe_list
                if recipe.id == recipe_id and recipe.is_publish == True
            ),
            None,
        )
        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND
        print(f"just checking :: {recipe.id} vs {recipe_list[recipe_id]}")
        # Update the recipe attributes with the new data
        recipe.name = data.get("name", recipe.name)
        recipe.description = data.get("description", recipe.description)
        recipe.num_of_servings = data.get("num_of_servings", recipe.num_of_servings)
        recipe.cook_time = data.get("cook_time", recipe.cook_time)
        recipe.directions = data.get("directions", recipe.directions)
        return recipe.data, HTTPStatus.OK


class RecipePublishResource(Resource):
    # publish recipe
    def put(self, recipe_id):
        recipe = next(
            (
                recipe
                for recipe in recipe_list
                if recipe.id == recipe_id
            ),
            None,
        )
        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND
        
        if recipe.is_publish:
            return {"message": "recipe already published!"}, HTTPStatus.NO_CONTENT
        else:
            recipe.is_publish = True
            return {"message": "recipe published successfully"}, HTTPStatus.NO_CONTENT

    # unpublish recipe
    def delete(self, recipe_id):
        recipe = next(
            (
                recipe
                for recipe in recipe_list
                if recipe.id == recipe_id
            ),
            None,
        )
        if recipe is None:
            return {"message": "recipe not found"}, HTTPStatus.NOT_FOUND
        
        recipe.is_publish = False

        return {}, HTTPStatus.NO_CONTENT
