from flask_app.config.conn import connectToMySQL
from flask_app.models import user, recipe, meal_type
from datetime import date, datetime, timedelta, time
from flask import flash

class Schedule:

    def  __init__(self, data) -> None:
        self.id = data['id']
        self.user_id = data['user_id']
        self.weekday = self.getweekday(data['weekday'])
        self.date = data['date']
        self.meal_type = data['m.name']
        self.preptime = data['pt.description']
        self.recipes = None
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        
    def getweekday(weekday_num):
        arr = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        return arr[weekday_num]

    @classmethod
    def add_schedule():
        pass

    @classmethod
    def edit_schedule():
        pass

    @classmethod
    def get_scheduled_recipes(cls, data):
        query = 'SELECT * FROM schedules s JOIN recipes r ON s.recipe_id = r.id  JOIN meal_types m ON s.meal_type_id = m.id JOIN preptimes pt ON s.preptime_id = pt.id JOIN recipes_cuisines rc ON r.id = rc.recipe_id  JOIN cuisines c ON rc.cuisine_id = c.id JOIN recipes_proteins rp ON r.id = rp.protein_id JOIN proteins p ON rp.protein_id = p.id WHERE s.id = %(user_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)

        schedule_days = []
        recipes = []
        proteins = []
        cuisines = []

        for day in results:
            if len(schedule_days) == 0:
                new_day = cls(day)
                schedule_days.append(new_day)
            elif day['id'] != new_day.id:
                new_day = cls(day)
                schedule_days.append(new_day)
            
            recipe_data = {
                'id': None

            }

            