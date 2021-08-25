from flask_app.config.conn import connectToMySQL
from flask_app.models import user
from datetime import date, datetime, timedelta, time
from flask import flash


class Preferences:
    
    def __init__(self, data) -> None:
        self.id = data['id']
        self.protein_id = data['protein_id']
        self.cuisine_id = data['cuisine_id']
        self.favorite_id = data['favorite_id']
        self.min = data['min']
        self.max = data['max']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']