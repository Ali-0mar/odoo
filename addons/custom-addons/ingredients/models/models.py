# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import threading
from concurrent.futures import ThreadPoolExecutor

thread_events = {}

def send_request(method, data, entity, event):
    try:
        data = {
            "query": method,
            "entity": entity,
            "data": data
        }
        res = requests.post(
            "http://127.0.0.1:3001/api/sync/",
            json=data
        )
        print(res)
    except Exception as e:
        print(e)
    finally:
        print("request done")
        event.set()


class Ingredients(models.Model):
    _name = 'ingredients.ingredients'
    _description = 'My Custom Ingredients module'

    name = fields.Char("Ingredient Name", required=True)
    type = fields.Selection(
        [
            ('meat', 'Meat'),
            ('vegetable', 'Vegetable'),
            ('fruit', 'Fruit')
        ],
        string="Ingredient Type"
    )
    calories = fields.Integer(string="Calories", default=0)
    description = fields.Text()
    image = fields.Binary(string="Image")

    @api.model
    def create(self, vals):
        errors = None
        result = None
        try:
            result = super(Ingredients, self).create(vals)
        except Exception as e:
            errors = e
        # Your custom logic here
        if result and not errors:
            data = {"id": result.id, **vals}
            event = threading.Event()
            thread = threading.Thread(target=send_request, args=("create", data, self._name, event))
            thread.daemon = True
            thread_events[thread] = event
            thread.start()

        return result

    def unlink(self):
        errors = None
        result = None
        try:
            result = super(Ingredients, self).unlink()
        except Exception as e:
            errors = e
        if result and not errors:
            data = {"id": self.ids[0]}
            thread = threading.Thread(target=send_request, args=("unlink", data, self._name))
            thread.daemon = True
            thread.start()
        return result

    def write(self, vals):
        errors = None
        result = None
        try:
            result = super(Ingredients, self).write(vals)
            print(f"write Called self is {self.ids}Result is ====={result} vals are-={vals}")
        except Exception as e:
            errors = e
        # Your custom logic here
        if result and not errors:
            data = {"id": self.ids[0], **vals}
            thread = threading.Thread(target=send_request, args=("update", data, self._name))
            thread.daemon = True
            thread.start()

        return result

