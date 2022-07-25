from flask_app import app, bcrypt
from flask import render_template, redirect, request, session

from flask_app.models import model_recipe, model_user


@app.route('/')
def index():
    if 'uuid' in session:
        return redirect('/dashboard')
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    if 'uuid' not in session:
        return redirect('/')
    context = {
        'all_recipes': model_recipe.Recipe.get_all(),
        'user': model_user.User.get_one({'id': session['uuid']})
    }
    return render_template('dashboard.html', **context)


