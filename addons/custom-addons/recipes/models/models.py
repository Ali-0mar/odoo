# -*- coding: utf-8 -*-

from odoo import models, fields, api


class recipes(models.Model):
    _name = 'recipes.recipes'
    _description = 'recipes.recipes'

    name = fields.Char("Recipe Name")
    description = fields.Text("Recipe Description")
    ingredients_ids = fields.Many2many('ingredients.ingredients', string="Ingredients", required=True)

    @api.depends('ingredients_ids', 'ingredients_ids.calories')
    def _total_calories(self):
        for recipe in self:
            total_calories = sum(ingredient.calories for ingredient in recipe.ingredients_ids)
            recipe.total_calories = total_calories

    total_calories = fields.Integer("Total Calories", compute="_total_calories")
