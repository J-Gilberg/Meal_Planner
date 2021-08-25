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
        self.meal_type_id = data['meal_type_id']
        self.meal_type = data['m.name']
        self.prep_time = data['pt.description']
        self.recipes = None
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

        
    def getweekday(weekday_num):
        arr = ['Monday','Tuesday','Wednesday','Thursday','Friday','Saturday','Sunday']
        return arr[weekday_num]

    @classmethod
    def add_schedule(cls, data):
        query = "INSERT INTO schedules (date, user_id, prep_time, meal_type_id) VALUES (%(date)s, %(user_id)s, %(prep_time)s, %(meal_type_id)s)"
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def edit_schedule(cls, data):
        query = "UPDATE schedules SET date = %(date)s, user_id = %(user_id)s, prep_time = %(prep_time)s, meal_type_id = %(meal_type_id)s WHERE id = %(id)s"
        connectToMySQL(cls.db).query_db(query, data)

    @classmethod
    def get_scheduled_recipes(cls, data):
        query = 'SELECT * FROM schedules s JOIN recipes_schedules rs ON s.id = rs.schedule_id JOIN recipes r ON s.recipe_id = r.id  JOIN meal_types m ON s.meal_type_id = m.id JOIN preptimes pt ON s.preptime_id = pt.id JOIN recipes_cuisines rc ON r.id = rc.recipe_id  JOIN cuisines c ON rc.cuisine_id = c.id JOIN recipes_diets rd ON r.id = rd.diet_id JOIN diets d ON rd.diets_id = d.id WHERE s.id = %(user_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)

        schedule_days = []
        recipes = []
        diets = []
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

    @classmethod
    def get_user_schedule(cls, data):
        query = 'SELECT * FROM schedules s WHERE s.id = %(user_id)s;'
        results = connectToMySQL(cls.db).query_db(query, data)
        user_schedule = []
        for s in results:
            user_schedule.append(cls(s))
        return user_schedule