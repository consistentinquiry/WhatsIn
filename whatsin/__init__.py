from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
app = Flask(__name__)
app.config['SECRET_KEY'] = '70dcb28ffcb20a5c76cbd7dd60b02050'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:johnsmells7@whatsin-db.cubhsslyixfb.eu-west-2.rds.amazonaws.com/whatsin_db'

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'

from whatsin import routes

