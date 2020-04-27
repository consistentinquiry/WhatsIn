#!/usr/bin/env python3

from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
import os
import datetime
from flask_sqlalchemy import SQLAlchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '70dcb28ffcb20a5c76cbd7dd60b02050'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'

db = SQLAlchemy(app)


class User(db.Model):
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
        return f"User('{self.username}', '{self.email}', '{self.image_file}', '{self.password}')"



class Fridge_item(db.Model):
    """ Models the attributes, methods and db structure of fridge_item objects """
    id = db.Column(db.Integer, primary_key=True)
    item_name = db.Column(db.String(20), unique=False, nullable=False)
    quantity = db.Column(db.Integer, nullable=False)
    use_by = db.Column(db.String(10), nullable=True)
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

logged_in = False

def run():
    """ Sets up paramters of web server & executes"""
    debug = os.environ.get('APP_DEBUG', True)
    host = os.environ.get('APP_HOST', '0.0.0.0')
    port = int(os.environ.get('APP_PORT', 80))

    app.run(debug=debug, host=host, port=port)

@app.route("/home")
def home():
    """ What occurs once the home route is called """
    print("Rendering home...")
    return render_template("base.html", fridge=fridge, cupboard=cupboard, logged_in=logged_in)

@app.route("/register", methods=['GET', 'POST'])
def register():
    """ What occues when the register route is called, a get request calls the render function and passes the register page template.
    If a valid form is posted then a message will flash informing the user of successful registration (as of yet it is non functional)
    and page will redirect to home."""
    print("[" + str(datetime.datetime.now()) + "]" + "instanciating form...")
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        print("[" + str(datetime.datetime.now())+ "]" + "The form is valid!")
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """ If a get request is submited the login page will be rendered. POST functionality yet to be implemented """
    form = LoginForm()
    return render_template('login.html', form=form)


if __name__ == "__main__":
    run()
