from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.users_models import User
from flask_app.models.recipes_models import Recipe 
from flask import render_template, redirect, request, session, flash
bcrypt = Bcrypt(app)

@app.route('/create_new', methods=['POST'])
def add_recipes():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/new')
    data = {
        "name" : request.form['name'], 
        "description" : request.form['description'],
        "instruction" : request.form['instruction']
    }
    print(data)
    recipe = Recipe.save(data)
    return redirect ("/dashboard")

@app.route('/recipes/edit')
def edit_recipes():
    if 'user_id' not in session:
        return redirect('/')
    if not Recipe.validate_recipe(request.form):
        return redirect('/recipes/edit')
    data = {
        "name" : request.form['name'], 
        "description" : request.form['description'],
        "instruction" : request.form['instruction']
    }
    print(data)
    recipe = Recipe.update(data)
    return redirect ("/dashboard", recipe = recipe)

@app.route('/recipes')
def recipes():
    if 'user_id' not in session:
        return redirect ('/')
    user = {
        'id' : session['user_id']
    }
    user = User.get_id(user)
    recipe = Recipe.get_one
    return render_template ("recipes.html", user = user, recipe=recipe)

@app.route('/recipes/new')
def show():
    if 'user_id' not in session:
        return redirect ('/')
    return render_template ("create_recipes.html")

@app.route('/destroy/message/<int:id>')
def destroy_message(id):
    data = {
        "id" : id
    }
    Recipe.destroy(data)
    return redirect('/dashboard')