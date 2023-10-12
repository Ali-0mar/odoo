# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class Recipes(http.Controller):
    @http.route('/recipes/recipes', auth='public')
    def index(self, **kw):
        return "Hello, Odoo"

    @http.route('/recipes/recipes/objects', auth='public')
    def list(self, **kw):
        recipes = request.env['recipes.recipes'].search([])

        # Convert the records into a list of dictionaries
        recipe_data = []
        for recipe in recipes:
            recipe_data.append({
                'id': recipe.id,
                'name': recipe.name,
                # Add other fields as needed
            })

        # Convert the data to JSON and return it as a response
        return json.dumps({'recipes': recipe_data})
    # @http.route('/recipes/recipes/objects/<model("recipes.recipes"):obj>', auth='public')
    # def object(self, obj, **kw):
    #     return http.request.render('recipes.object', {
    #         'object': obj
    #     })
