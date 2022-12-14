from flask_app.config.mysqlconnection import connectToMySQL 
from flask_app import DATABASE
from flask import flash
from flask_app.utility import utilities
from flask_app.models import user_model
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$') 

class Recipe:
    def __init__(self,data):
        self.id = data['id']
        self.name = data['name']
        self.description = data['description']
        self.instructions = data['instructions']
        self.under = data['under']
        self.date = data['date']
        self.created_at = data['created_at']
        self.updated_at = data['updated_at']
        self.user_id = data['user_id']


    @classmethod
    def create(cls,data):
        query="""
        INSERT INTO recipes (name,description,instructions,date,user_id,under)
        VALUES (%(name)s,%(description)s,%(instructions)s,%(date)s,%(user_id)s,%(under)s);
        """

        return connectToMySQL(DATABASE).query_db(query,data)


#classmethod to delete
    @classmethod
    def delete(cls,data):
        query="""
        DELETE FROM recipes
        where recipes.id = %(id)s
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    @classmethod
    #get all the many with its one
    def get_all(cls):
        query="""
        SELECT *
        FROM recipes
        LEFT JOIN users on users.id = recipes.user_id;
        """
        results = connectToMySQL(DATABASE).query_db(query)
        print("-------------------get all results incoming from recipe model--------------------")
        print(results)
        all_recipes = []
        if results:
            for row in results:
                this_recipe = cls(row) #creates one recipe
                user_data = {
                    **row,
                    'id': row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['updated_at']
                }	
                this_user = user_model.User(user_data) #creates a user instance off the data
                #provided
                this_recipe.creator = this_user #creates a new attribute called creator
                #that has the user associated with the recipe
                all_recipes.append(this_recipe)
        return all_recipes

    #get one recipe with the user who created it.
    @classmethod
    def get_one(cls,data):
        query="""
        SELECT *
        FROM recipes
        LEFT JOIN users on recipes.user_id = users.id
        WHERE recipes.id = %(id)s
        """
        results = connectToMySQL(DATABASE).query_db(query,data)
        if results:
            recipe_instance = cls(results[0])
            for row in results:
                user_data = {
                    **row,
                    'id' : row['users.id'],
                    'created_at': row['users.created_at'],
                    'updated_at': row['users.updated_at']
                }
                user_instance = user_model.User(user_data)
                recipe_instance.creator = user_instance
                return recipe_instance
        return 

    #allows the user to edit the recipe
    @classmethod
    def update(cls,data):
        query="""
        UPDATE recipes
        SET name = %(name)s,description = %(description)s,instructions = %(instructions)s,date = %(date)s,under = %(under)s
        WHERE recipes.id = %(id)s
        """
        return connectToMySQL(DATABASE).query_db(query,data)

    
    #vaidations for the recipes
    @staticmethod
    def validator(form_data):
        is_valid = True
        if len(form_data['name']) < 3:
            is_valid = False
            flash("Name of the recipe must be at least 3 characters", "name")
        if len(form_data['description']) < 3:
            is_valid = False
            flash("Description must be at least 3 characters", "description")
        if len(form_data['instructions']) < 3:
            is_valid = False
            flash("Instructions must be at least 3 characters", "instructions")
        if len(form_data['date']) < 1:
            is_valid = False
            flash("Date required", "date")
        if "under" not in form_data:
            flash("you need to select whether the cook-time is under 30 mins or not", "time")
            is_valid = False
        return is_valid
