# import the function that will return an instance of a connection
from flask_app.config.mysqlconnection import connectToMySQL
from flask_app import DATABASE, bcrypt
from flask import flash, session
from flask_app.models import model_user

DATABASE = 'recipe_db'

# model the class after the friend table from our database



class Recipe:
    def __init__(self, data):
        # ADD attributes for every column in our database table
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.date_made = data['date_made']
        self.under = data['under']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.created_by = {}

    # Create
    @classmethod
    def create(cls, data: dict) -> int:
        # add all column names and add all values
        query = "INSERT INTO recipes (name, description, instructions, date_made, under, user_id, created_at, updated_at) VALUES (%(name)s, %(description)s, %(instructions)s, %(date_made)s, %(under)s,  %(user_id)s, NOW(), NOW());"
        # returns the id/row of the new user added to the db
        recipe_id = connectToMySQL(DATABASE).query_db(query, data)
        return recipe_id

    # Read
    @classmethod
    def get_one(cls, data: dict) -> list:
        query = "SELECT * FROM recipes LEFT  JOIN users ON users.id = recipes.user_id where recipes.id=%(id)s;"
        results = connectToMySQL(DATABASE).query_db(query, data)
        if results:
            dict = results[0]
            recipe = cls(dict)
            user_data = {
                'id': dict['users.id'],
                    'created_at': dict['users.created_at'],
                    'updated_at': dict['users.updated_at'],
                    'first_name': dict['first_name'],
                    'last_name': dict['last_name'],
                    'email': dict['email'],
                    'pwd': dict['pwd'],
                }
            user = model_user.User(user_data)
            recipe.created_by = user
            return recipe
        return False

    @classmethod
    def get_all(cls) -> list:
        query = 'SELECT * FROM recipes JOIN users ON users.id = recipes.user_id;'
        results = connectToMySQL(DATABASE).query_db(query)
        if results:
            all_recipes = []
            for dict in results:
                recipe = cls(dict)
                user_data = {
                    'id': dict['users.id'],
                    'created_at': dict['users.created_at'],
                    'updated_at': dict['users.updated_at'],
                    'first_name': dict['first_name'],
                    'last_name': dict['last_name'],
                    'email': dict['email'],
                    'pwd': dict['pwd'],
                }
                user = model_user.User(user_data)
                recipe.created_by = user
                all_recipes.append(recipe)
            return all_recipes
        return []

    # Update
    @classmethod
    def update_one(cls, data: dict) -> None:
        query = "UPDATE recipes SET name = %(name)s, description = %(description)s, instructions = %(instructions)s, date_made = %(date_made)s, under = %(under)s, updated_at = NOW() WHERE id = %(id)s;"
        print('-------------update-----------')
        print(query)
        result = connectToMySQL(DATABASE).query_db(query, data)
        print('-------------update-----------')
        print(result)
        return result

    # Delete 
    @classmethod
    def delete_one(cls, data: dict) -> None:
        # ADD COLUMNS = values for every column that you wish to change in to db
        query = "DELETE FROM recipes WHERE id = %(id)s"
        return connectToMySQL(DATABASE).query_db(query, data)

    @staticmethod
    def validator(data: dict) -> bool:
        is_valid = True

        if len(data['name']) < 1:
            flash('field is required', 'err_recipes_name')
            is_valid = False

        if len(data['description']) < 1:
            flash('field is required', 'err_recipes_description')
            is_valid = False
        
        if len(data['instructions']) < 1:
            flash('field is required', 'err_recipes_instructions')
            is_valid = False
        return is_valid

