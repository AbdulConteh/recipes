import re
from flask import flash
from flask_app.config.mysqlconnection import connectToMySQL
db = "recipes_assignment_db"

class Recipe:
    def __init__(self, data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instruction = data['instruction']
        self.under30 = data['under30']
        self.date_made = data['date_made']
        self.user_id = data['user_id']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']

    @classmethod 
    def save(cls, data):
        query = """
            INSERT INTO recipes (name, description, instruction, under30, date_made, user_id)
            VALUES (%(name)s, %(description)s, %(instruction)s, %(under30)s, %(date_made)s, %(user_id)s)
        """
        result = connectToMySQL(db).query_db(query, data)
        return result

    @classmethod
    def get_all(cls):
        query = "SELECT * FROM recipes"
        results = connectToMySQL(db).query_db(query)
        recipe = []
        for recipes in results:
            recipe.append( cls (recipes))
        return recipe

    @classmethod
    def get_one(cls, data):
        query = " SELECT * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        return cls( results[0])

    @classmethod 
    def update(cls, data):
        query = """
            UPDATE recipes SET name=%(name)s, description=%(description)s, instruction=%(instruction)s, 
            under30=%(under30)s, date_made=%(date_made)s, updated_at=NOW() WHERE id = %(id)s;
        """
        return connectToMySQL(db).query_db(query, data)

    @classmethod 
    def get_id(cls, data):
        query = "SELECT * FROM recipes WHERE id = %(id)s;"
        results = connectToMySQL(db).query_db(query, data)
        if len(results) < 1:
            return False
        return cls(results[0])

    @classmethod 
    def destroy(cls, data):
        query = "DELETE * FROM recipes WHERE id = %(id)s"
        results = connectToMySQL(db).query_db(query, data)
        return results

    @staticmethod
    def validate_recipe( Recipes ):
        is_valid = True
        if len(Recipes['name']) < 2:
            flash("Name must be longer than 2 characters. Please try again!", "recipes")
            is_valid = False
        if len(Recipes['description']) < 2:
            flash("Description must be longer than 2 characters. Please try again!", "recipes")
            is_valid = False
        if len(Recipes['instruction']) < 2:
            flash("Instructions must be longer than 2 characters. Please try again!", "recipes")
            is_valid = False
        return is_valid