from flask_app.config.conn import connectToMySQL
from flask import flash
import re
class User:

    db = 'meal_planner_schema'
    
    def __init__(self,data):
        self.id = data['id']
        self.username = data['username']
        self.email = data['email']
        self.password = data['password']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    

    @classmethod
    def get_user(cls,data):
        query = "SELECT * FROM users WHERE id = %(id)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        return User(result[0])
        
    @classmethod
    def get_by_email(cls,data):
        query = "SELECT * FROM users WHERE email = %(email)s;"
        result = connectToMySQL(cls.db).query_db(query,data)
        print(result)
        if len(result) < 1:
            return False
        return cls(result[0])

    @classmethod
    def save(cls,data):
        query = "INSERT INTO users (email, username, password) VALUES(%(email)s,%(username)s,%(password)s);"
        return connectToMySQL(cls.db).query_db(query, data)

    @staticmethod
    def validate_user(user):
        EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$")
        # FNAME_REGEX = re.compile(r"^[A-Z]{1}[\w. '-]{1,254}$")
        USERNAME_REGEX = re.compile(r"^[\w. '-]{2,45}$")

        data = {
            'email': user['email']
        }
        is_valid = True # we assume this is true

        if not USERNAME_REGEX.match(user["username"]): 
            flash("Invalid Last Name: name only contain special the characters: periods, spaces, darshes, apostophies, and accents")
            is_valid = False

        if not EMAIL_REGEX.match(user['email']) or not len(user['email']) < 255: 
            flash("Invalid email address!")
            is_valid = False

        if  User.get_by_email(data):
            flash("Invalid email address: email is already linked to an account")
            is_valid = False

        if not len(user['password']) >= 8 or not len(user['password']) < 255:
            flash("Invalid Password: password must be at least 8 characters")
            is_valid = False

        if not user['password'] == user['conf_password']:
            flash("Invalid Password: password must be at least 8 characters")
            is_valid = False
        return is_valid
