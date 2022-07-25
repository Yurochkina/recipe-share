# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
from flask_app.models import model_recipe
import re	# the regex module
# create a regular expression object that we'll use later   
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')

DATABASE = 'recipe_db'

# model the class after the friend table from our database



class User:
    def __init__(self, data):
        # ADD attributes for every column in our database table
        self.id = data['id']
        self.first_name = data['first_name']
        self.last_name = data['last_name']
        self.email = data['email']
        self.pwd = data['pwd']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.recipes = []

    # Create
    @classmethod
    def create(cls, data: dict) -> int:
        # add all column names and add all values
        query = "INSERT INTO users (first_name, last_name, email, pwd) VALUES (%(first_name)s, %(last_name)s, %(email)s, %(pwd)s);"
        # returns the id/row of the new user added to the db
        user_id = connectToMySQL(DATABASE).query_db(query, data)
        print(user_id)
        return user_id

    # Read
    @classmethod
    def get_one(cls, data: dict) -> list:
        query = "SELECT * FROM users WHERE id = %(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_one_by_email(cls, data: dict) -> list:

        query = "SELECT * FROM users WHERE email = %(email)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            return cls(results[0])
        return False

    @classmethod
    def get_all(cls) -> list:
        query = "SELECT * FROM users;"
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_users = []
            for user in results:
                all_users.append(cls(user))
            return all_users
        return False

    # Update
    @classmethod
    def update_one(cls, data: dict) -> None:
        query = "UPDATE users SET first_name = %(first_name)s, last_name = %(last_name)s, email = %(email)s WHERE id = %(id)s;"
        return connectToMySQL(DATABASE).query_db(query, data)

    # Delete 
    @classmethod
    def delete_one(cls, data: dict) -> None:
        # ADD COLUMNS = values for every column that you wish to change in to db
        query = "DELETE FROM users WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validator(data: dict) -> bool:
        print(data)
        is_valid = True

        if len(data['first_name']) < 1:
            flash('field is required', 'err_users_first_name')
            is_valid = False

        if len(data['last_name']) < 1:
            flash('field is required', 'err_users_last_name')
            is_valid = False
        
        if len(data['email']) < 1:
            flash('field is required', 'err_users_email')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'err_users_email')
            is_valid = False
        else:
            potential_user = User.get_one_by_email({'email': data['email']})
            if potential_user:
                flash('Email already in use', 'err_users_email')
                is_valid = False

        if len(data['pwd']) < 1:
            flash('field is required', 'err_users_pwd')
            is_valid = False

        if len(data['confirm_pw']) < 1:
            flash('field is required', 'err_users_confirm_pwd')
            is_valid = False

        elif data['pwd'] != data['confirm_pw']:
            flash('Passwords do not match', 'err_users_confirm_pw')
            is_valid = False


        return is_valid

    @staticmethod
    def validator_login(data: dict) -> bool:
        print(data)
        is_valid = True
        
        if len(data['email']) < 1:
            flash('field is required', 'err_users_email_login')
            is_valid = False
        elif not EMAIL_REGEX.match(data['email']): 
            flash("Invalid email address!", 'err_users_email_login')
            is_valid = False
        else:
            potential_user = User.get_one_by_email({'email': data['email']})
            if not potential_user:
                flash('Invalid Credentials', 'err_users_email_login')
                is_valid = False

            # check the hash
            elif not bcrypt.check_password_hash(potential_user.pwd, data['pwd']):
                flash('Invalid Credentials!!', 'err_users_email_login')
                is_valid = False
            else:
                # store the id into the session
                session['uuid'] = potential_user.id


        if len(data['pwd']) < 1:
            flash('field is required', 'err_users_pwd_login')
            is_valid = False


        return is_valid

