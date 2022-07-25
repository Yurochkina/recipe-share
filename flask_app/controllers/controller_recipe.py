from flask_app import app, bcrypt
from flask import render_template, redirect, request, session

from flask_app.models import model_recipe, model_user


@app.route('/recipes/new')
def recipes_new():
    return render_template('new_recipe.html')

@app.route('/recipes/create', methods=['POST'])
def recipes_create():
    # validations
    if not model_recipe.Recipe.validator(request.form):
        return redirect('/recipes/new')

    # create recipe
    data = {
        **request.form,
        'user_id': session['uuid']
    }
    model_recipe.Recipe.create(data)
    return redirect('/')

# Display route
@app.route('/recipes/<int:id>')
def recipe_show(id):
    context = {
        'recipe': model_recipe.Recipe.get_one({'id': id}),
        'user': model_user.User.get_one({'id': session['uuid']})
    }
    return render_template('view_recipe.html', **context)

# Display route
@app.route('/recipes/<int:id>/edit')
def instrument_edit(id):
    context = {
        'recipe': model_recipe.Recipe.get_one({'id': id})
    }
    return render_template('edit_recipe.html', **context)

# ACTION ROUTE
@app.route('/recipes/<int:id>/update', methods=['POST'])
def recipe_update(id):
    # validations
    if not model_recipe.Recipe.validator(request.form):
        return redirect(f'/recipes/{id}/edit')
    data = {
        **request.form,
        'id': id
    }
    print(data)
    model_recipe.Recipe.update_one(data)
    return redirect('/dashboard')

@app.route('/recipes/<int:id>/delete')
def recipe_delete(id):
    model_recipe.Recipe.delete_one({'id': id})
    return redirect('/')