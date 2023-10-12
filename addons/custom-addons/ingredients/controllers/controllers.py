# -*- coding: utf-8 -*-
from odoo import http
from odoo.http import request
import json


class Ingredients(http.Controller):
    @http.route('/ingredients/ingredients', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/ingredients/ingredients/objects', auth='public')
    def list(self, **kw):
        return http.request.render('ingredients.listing', {
            'root': '/ingredients/ingredients',
            'objects': http.request.env['ingredients.ingredients'].search([]),
        })

    @http.route('/ingredients/ingredients/objects/<model("ingredients.ingredients"):obj>', auth='public')
    def object(self, obj, **kw):
        return http.request.render('ingredients.object', {
            'object': obj
        })

    @http.route('/ingredients/ingredients/create', auth='public', type='json', methods=['POST'], csrf=False)
    def create(self, **kw):
        try:
            # Parse the JSON data from the request
            data = json.loads(request.httprequest.data)

            # Create a new ingredient record
            new_ingredient = request.env['ingredients.ingredients'].create({
                'name': data.get('name'),
                'type': data.get('type'),
                'calories': data.get('calories'),
                'description': data.get('description'),
                # Add other fields as needed
            })

            # Return a JSON response indicating success
            return {
                'status': 'success',
                'message': 'Ingredient created successfully',
                'ingredient_id': new_ingredient.id,
            }
        except Exception as e:
            # Return a JSON response in case of an error
            return {
                'status': 'error',
                'message': str(e),
            }
