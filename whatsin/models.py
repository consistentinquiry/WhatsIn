from whatsin import db, login_manager
from datetime import datetime
from flask_login import UserMixin

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    """ Models the attributes, methods and db structure of user objects """
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(50), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    fridge_items = db.relationship('Fridge_item', backref='fridge_item_owner', lazy=True)
    cupboard_items = db.relationship('Cupboard_item', backref='cupboard_item_owner', lazy=True)
    


    def __repr__(self):
        """Return a string representation of the object """
        return f"User('{self.id}', '{self.username}', '{self.email}', '{self.image_file}', '{self.password}')"



class Fridge_item(db.Model):
    """ Models the attributes, methods and db structure of fridge_item objects """
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(20), unique=False, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    use_by = db.Column(db.DateTime,  nullable=True)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        """Return a string representation of the object """
        return f"Fridge item('{self.item_name}', '{self.quantity}', '{self.use_by}', '{self.image_file}')"


class Cupboard_item(db.Model):
    """ Models the attributes, methods and db structure of cupboard_item objects """
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(20), unique=False, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    owner = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)  #lowercase as this references table name not model name

    def __repr__(self):
        """Return a string representation of the object """
        return f"Cupboard item('{self.item_name}', '{self.quantity}', '{self.image_file}')"

