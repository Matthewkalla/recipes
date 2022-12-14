from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

#create a new recipe
@app.route('/recipes/new')
def new_recipe_form():
    if 'user_id' not in session:
        flash("user not logged in", "not_logged")
        return redirect('/')
    return render_template("recipes_new.html")


@app.route('/recipes/create', methods=['POST'])
def create_recipe():
    if 'user_id' not in session:
        flash("user not logged in", "not_logged")
        return redirect('/')
    if not Recipe.validator(request.form):
        print("----------------------------------------------form data")
        print(request.form)
        return redirect('/recipes/new')
    party_data ={
        **request.form,
        'user_id': session['user_id']
    }
    print('------------------party data incoming----------------------')
    print(party_data['under'])
    recipe_id = Recipe.create(party_data)
    return redirect(f'/recipes/{recipe_id}/view')


#creates the route to view
@app.route('/recipes/<int:id>/view')
def get_recipe(id):
    if 'user_id' not in session:
        flash("user not logged in", "not_logged")
        return redirect('/')
    user_data = {
        'id' : session['user_id']
    }
    logged_user = User.get_by_id(user_data)
    one_recipe = Recipe.get_one({'id':id})
    return render_template("recipes_one.html",one_recipe=one_recipe, logged_user=logged_user)


#creates the route to edit
@app.route('/recipes/<int:id>/edit')
def edit_page(id):
    if 'user_id' not in session:
        flash("user not logged in", "not_logged")
        return redirect('/')
    one_recipe = Recipe.get_one({'id':id})
    return render_template("recipes_edit.html", one_recipe=one_recipe)


#the route to delete a recipe
@app.route('/recipes/<int:id>/delete')
def remove(id):
    if 'user_id' not in session:
        flash("user not logged in", "not_logged")
        return redirect('/')
    data = {'id':id}


    #THIS NEXT PART IS NOT BEING GRADED ON
    #DON'T WORRY
    this_recipe = Recipe.get_one(data)
    if not this_recipe.user_id == session['user_id']:
        flash("Not yours, hands off!!!", "wrong_user")
        return redirect('/dashboard')
    Recipe.delete(data)

    return redirect('/dashboard')

#the route to update the recipe
@app.route('/recipes/<int:id>/update', methods=['POST'])
def update_recipe(id):
    if 'user_id' not in session:
        flash("user not logged in", "not_logged")
        return redirect('/')
    if not Recipe.validator(request.form):
        return redirect(f"/recipes/{id}/edit")
    update_data = {
        **request.form,
        'id':id
    }
    Recipe.update(update_data)
    return redirect("/dashboard")

#route to view all the recipes that belong to the logged in user
@app.route('/my_recipes')
def show_users_receipes():
    if 'user_id' not in session:
        flash("user not logged in", "not_logged")
        return redirect('/')
    logged_user = User.get_by_id({'id':session['user_id']})
    print("_____________________DEBUGGGINGGGGG__________________________")
    print(logged_user.recipes)
    return render_template("my_recipes.html", logged_user=logged_user)