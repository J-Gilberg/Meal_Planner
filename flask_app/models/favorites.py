from flask_app.config.conn import connectToMySQL
from flask_app.models import user
from datetime import date, datetime, timedelta, time
from flask import flash

class Favorites:

    def __init__(self, data):
        self.id = data['id']
        self.user_id = data['user_id']
        self.recipe_id = data['recipe_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
