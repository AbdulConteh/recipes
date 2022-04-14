from flask_app import app
from flask_bcrypt import Bcrypt
from flask_app.models.users_models import User
from flask_app.models.recipes_models import Recipe 
from flask import render_template, redirect, request, session, flash
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/create', methods=['POST'])
def create():
    if not User.validate_user(request.form):
        return redirect('/')
    data = {
        "first_name" : request.form["first_name"],
        "last_name" : request.form["last_name"],
        "email" : request.form["email"],
        "password" : bcrypt.generate_password_hash(request.form["password"])
    }
    id = User.save(data)
    session['user_id'] = id
    return redirect ('/')

@app.route('/login', methods=["POST"])
def get_account():
    data = { 
        "email" : request.form["email"]
    }
    user = User.get_account(data)
    if not user:
        flash("Unregistered Email. Please try again!", "login")
        return redirect('/')
    print(user.password)
    if not bcrypt.check_password_hash(user.password, request.form["password"]):
        flash("Invalid password", "login")
        return redirect('/')
    session['user_id'] = user.id
    return redirect('/dashboard')

@app.route('/dashboard')
def profile():
    if 'user_id' not in session:
        return redirect ('/')
    data = {
        'id' : session['user_id']
    }
    user = User.get_id(data)
    recipe = Recipe.get_all()
    return render_template("dashboard.html", user=user, recipe = recipe)

@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')