from flask_app.config.conn import connectToMySQL
from flask_app.models import user
from datetime import date, datetime, timedelta, time
from flask import flash


class Cuisine:

    db = 'meal_planner_schema'

    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.category_id = data['category_id']
        self.categorr_name = data['cc.name']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod
    def get_all_cuisine(cls):
        query = 'SELECT * FROM cuisines c LEFT JOIN cuisines cc ON c.category_id = cc.id;'
        results = connectToMySQL(cls.db).query_db(query)
        cuisines = []
        for c in results:
            cuisines.append(cls(c))
        return cuisines
