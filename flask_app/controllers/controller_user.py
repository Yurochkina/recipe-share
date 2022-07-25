from flask_app import app, bcrypt
from flask import render_template, redirect, request, session

# this imports the model file
from flask_app.models import model_user

# Display route
@app.route('/user/login', methods=['POST'])
def user_new():
    model_user.User.validator_login(request.form)
    return redirect('/')

@app.route('/user/logout')
def logout_user():
    del session['uuid']
    return redirect('/')


# ACTION ROUTE
@app.route('/user/create', methods=['POST'])
def user_create():
    # validations
    if not model_user.User.validator(request.form):
        return redirect('/dashboard')

    # hashing
    hash_pw = bcrypt.generate_password_hash(request.form['pwd'])
    data = {
        **request.form,
        'pwd': hash_pw
    }

    # create my user
    id = model_user.User.create(data)

    # store user id in session
    session['uuid'] = id

    return redirect('/dashboard')

# Display route
@app.route('/user/<int:id>')
def user_show(id):
    return render_template('user_show.html')

# Display route
@app.route('/user/<int:id>/update', methods=['POST'])
def user_edit(id):
    return render_template('user_edit.html')

# ACTION ROUTE
@app.route('/user/<int:id>/update', methods=['POST'])
def user_update(id):
    return redirect('/')

@app.route('/user/<int:id>/delete')
def user_delete(id):
    return redirect('/')