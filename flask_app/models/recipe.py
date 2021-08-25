from flask_app.config.conn import connectToMySQL
from flask_app.models import user
from datetime import date, datetime, timedelta, time
from flask import flash

class Recipe:

    db = 'meal_planner_schema'

    def __init__(self, data):
        self.id = data['id']
        self.title = data['title']
        self.description = data['description']
        self.prep_time = data['prep_time']
        self.meal_type = data['name']
        self.proteins = None
        self.cuisines = None
        # need to add more variables here later

    @classmethod
    def create_recipe(cls, data):
        time = f"{data['prep_time']} {data['time_metric']}"
        query = f"INSERT INTO recipes (title, description, prep_time, meal_type_id) VALUES (%(title)s, %(description)s, '{time}' , %(meal_type_id)s);"
        new_recipe_id = connectToMySQL(cls.db).query_db(query, data)
        query = f'INSERT INTO recipes_diets (recipe_id, diet_id) VALUES ({new_recipe_id}, %(diet_id)s);'
        connectToMySQL(cls.db).query_db(query, data)
        query = f'INSERT INTO recipes_cuisines (recipe_id, cuisine_id) VALUES ({new_recipe_id}, %(cuisine_id)s);'
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_recipes(cls):
        query = 'SELECT * FROM recipes r JOIN meal_types m ON r.meal_type_id = m.id;'
        results = connectToMySQL(cls.db).query_db(query)
        recipes = []
        for recipe in results:
            recipes.append(cls(recipe))
        print(recipes[0].title)
        return recipes
    
    @classmethod
    def get_single_recipe(cls,data):
        query = 'SELECT * FROM recipes WHERE id_recipes = %(id_recipes)s'
        results = connectToMySQL(cls.db).query_db(query, data)
        recipe = Recipe(results[0])
        return recipe

    @staticmethod
    def recipe_validator(data):
        is_valid = True
        print(data)
        # print(data['quantity'])
        # if len(data['title']) < 2:
        #     flash('please provide a title greater than or equal to 2 characters')
        #     is_valid = False
        # if len(data['title']) > 255:
        #     flash('please provide a title less than or equal to 255 characters')
        #     is_valid = False
        # if len(data['description']) < 10:
        #     flash('please provide a description greater than or equal to 10 characters')
        #     is_valid = False
        # if len(data['description']) > 500:
        #     flash('please provide a description less than or equal to 500 characters')
        #     is_valid = False
        return is_valid
