from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_uploads import UploadSet, configure_uploads, IMAGES

app = Flask(__name__)
app.config['SECRET_KEY'] = ''
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:@whatsin-db.cubhsslyixfb.eu-west-2.rds.amazonaws.com/whatsin_db'
app.config['UPLOADED_PHOTOS_DEST'] = 'whatsin/static/recipt_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'gif', 'jpeg' }

photos = UploadSet('photos', IMAGES)

configure_uploads(app, photos)

db = SQLAlchemy(app)

bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = 'login'


from whatsin import routes   #
from whatsin import watcher  #would this be the correct way of creating a watcher object,
                            #it needs to be accessed throughout the application 

