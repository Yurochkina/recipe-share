from flask_bcrypt import Bcrypt
from flask import Flask
app = Flask(__name__)
app.secret_key = "12931812-xasx22-123sd-22"
DATABASE = 'recipe_db'

bcrypt = Bcrypt(app)
