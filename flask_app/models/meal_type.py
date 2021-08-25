from flask_app.config.conn import connectToMySQL
from flask_app.models import user
from datetime import date, datetime, timedelta, time
from flask import flash

class Meal_type:

    db = 'meal_planner_schema'

    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_meal_types(cls):
        query = 'SELECT * FROM meal_types;'
        results = connectToMySQL(cls.db).query_db(query)
        meal_types = []
        for m in results:
            meal_types.append(cls(m))
        return meal_types