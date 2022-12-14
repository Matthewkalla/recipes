from flask_app import app
from flask import render_template, redirect, request, flash, session
from flask_bcrypt import Bcrypt
from flask_app.models.user_model import User
from flask_app.models.recipe_model import Recipe

bcrypt = Bcrypt(app)

#home page
@app.route('/')
def index():
    if 'user_id' in session:
        return redirect('/dashboard')
    return render_template("index.html")

#register the user
@app.route('/users/register', methods=['POST'])
def reg_user():
    if not User.validator(request.form):
        return redirect('/')

    hashed_pass = bcrypt.generate_password_hash(request.form['password'])
    data = {
        **request.form,
        'password':hashed_pass,
        'conf_pass': hashed_pass
    }
    session['user_id'] = User.create(data)
    return redirect('/dashboard')

#logs in the user
@app.route('/users/login', methods=['POST'])
def log_user():
    user_in_db = User.get_by_email(request.form)
    if not user_in_db:
        flash("invalid credentials", "log")
        return redirect('/')
    if not bcrypt.check_password_hash(user_in_db.password, request.form['password']):
        flash("invalid credentials", "log")
        return redirect('/')
    session['user_id'] = user_in_db.id
    return redirect('/dashboard')

#logs out the user
@app.route('/users/logout')
def log_out():
    del session['user_id']
    return redirect('/')

#the dashboard
@app.route('/dashboard')
def dashboard():

    if 'user_id' not in session:
        flash("you don't belong there!")
        return redirect('/')
    data = {
        'id': session['user_id']
    }
    logged_user = User.get_by_id(data)
    print("------------------------these are all the recipes------------------")
    all_recipes = Recipe.get_all()
    print(all_recipes)
    return render_template("dashboard.html",logged_user=logged_user, all_recipes=all_recipes)


