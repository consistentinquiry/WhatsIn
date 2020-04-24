#!/usr/bin/env python3

from flask import Flask, render_template, flash, redirect, url_for
from forms import RegistrationForm, LoginForm
import os
import sqlalchemy


app = Flask(__name__)
app.config['SECRET_KEY'] = '70dcb28ffcb20a5c76cbd7dd60b02050'
fridge = [
        {
            'id': '0',
            'item_name': 'cheese',
            'quantity': '1',
            'use_by': '1-apr'
        },
        {
            'id': '1',
            'item_name': 'bacon',
            'quantity': '1',
            'use_by': '1-apr'
        },
        {
            'id': '2',
            'item_name': 'opened beans',
            'quantity': '1',
            'use_by': '1-apr'
        },
        {
            'id': '3',
            'item_name': 'peach',
            'quantity': '2',
            'use_by': '1-apr'
        },
    ]

cupboard = [
        {
            'id': '0',
            'item_name': 'beans',
            'quantity': '3'
        },
        {
            'id': '1',
            'item_name': 'spam',
            'quantity': '2'
        }
    ]

logged_in = False

def run():
    debug = os.environ.get('APP_DEBUG', True)
    host = os.environ.get('APP_HOST', '0.0.0.0')
    port = int(os.environ.get('APP_PORT', 80))

    app.run(debug=debug, host=host, port=port)

@app.route("/home")
def home():
    print("Rendering home...")
    return render_template("base.html", fridge=fridge, cupboard=cupboard, logged_in=logged_in)

@app.route("/register", methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        print("Redirecting..")
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    return render_template('login.html', form=form)


if __name__ == "__main__":
    run()
