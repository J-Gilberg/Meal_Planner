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
        self.meal_type = data['meal_type']
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
    # connectToMySQL(cls.db).query_db(query, data)




        # for painting in results:
        #     new_painting = Painting(painting)
        #     paintings.append(new_painting)

        #     new_user = {
        #         'id': painting['u.id']
        #         ,'first_name': painting['first_name']
        #         ,'last_name': painting['last_name']
        #         ,'email': painting['email']
        #         ,'password': None
        #         ,'created_at': painting['created_at']
        #         ,'updated_at': painting['updated_at']
        #     }
        #     new_painting.user = login_reg.User(new_user)
        # return paintings

    @classmethod
    def get_painting(cls, data):
        query = 'SELECT * FROM paintings p JOIN users u ON p.user_id = u.id WHERE p.id = %(id)s;'
        result = connectToMySQL(cls.db).query_db(query,data)
        query_two = 'SELECT COUNT(painting_id) c FROM purchases WHERE painting_id = %(id)s;'
        result_two = connectToMySQL(cls.db).query_db(query_two,data)

        new_user = {
            'id': result[0]['u.id']
            ,'first_name': result[0]['first_name']
            ,'last_name': result[0]['last_name']
            ,'email': result[0]['email']
            ,'password': None
            ,'created_at': result[0]['created_at']
            ,'updated_at': result[0]['updated_at'] 
        }
        
        new_painting = Painting(result[0])
        new_painting.user = login_reg.User(new_user)
        new_painting.number_purchased = int(result_two[0]['c'])
        return new_painting

    @classmethod
    def add_painting(cls,data):
        query = 'INSERT INTO paintings (title, description, price, quantity, user_id) VALUES(%(title)s,%(description)s,%(price)s,%(quantity)s,%(user_id)s);'
        connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def delete_painting(cls,data):
        query = 'DELETE FROM paintings WHERE id = %(id)s;'
        connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def edit_painting(cls, data):
        query = 'UPDATE paintings SET title = %(title)s, description = %(description)s, price = %(price)s, quantity = %(quantity)s WHERE id = %(id)s;'
        connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def add_purchase(cls, data):
        query = 'INSERT INTO purchases (user_id, painting_id) VALUES(%(user_id)s,%(painting_id)s);'
        connectToMySQL(cls.db).query_db(query,data)

    @classmethod
    def get_user_purchases(cls,data):
        query = 'SELECT * FROM purchases pp JOIN paintings p ON pp.painting_id = p.id JOIN users uu ON p.user_id = uu.id WHERE pp.user_id = %(id)s;'
        results = connectToMySQL(cls.db).query_db(query,data)

        purchases = []
        for painting in results:
            new_painting = Painting(painting)
            

            new_user = {
                'id': painting['id']
                ,'first_name': painting['first_name']
                ,'last_name': painting['last_name']
                ,'email': painting['email']
                ,'password': None
                ,'created_at': painting['created_at']
                ,'updated_at': painting['updated_at'] 
            }

            new_painting.user = login_reg.User(new_user)
            purchases.append(new_painting)
        return purchases