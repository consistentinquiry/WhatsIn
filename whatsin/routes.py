from whatsin.models import User, Fridge_item, Cupboard_item
from flask import render_template, flash, redirect, url_for, request, abort
#from flask.ext.login import login_required, login_user
from whatsin.forms import RegistrationForm, LoginForm, AddToFridgeForm, AddToCupboardForm, FridgeItemForm, CupboardItemForm, ViewAccount
from whatsin import app, db, bcrypt, watcher, photos, ALLOWED_EXTENSIONS #imports from run.py
import os
import datetime
from datetime import date
from flask_login import login_user, current_user, logout_user, login_required
from whatsin.watcher import Watcher
from werkzeug.utils import secure_filename


watcher0 = Watcher()
watcher0.run()
#fridge = [
#        {
#            'id': '0',
#            'item_name': 'Open spam',
#            'quantity': '2',
#            'use_by': '05-may'
#        }]
#
#cupboard = [
#        {
#            'id': '0',
#            'item_name': 'Spam',
#            'quantity': '1',
#        },
#        {
#            'id': '1',
#            'item_name': 'Ham',
#            'quantity': '2'
#        }]


@app.route("/home")
def home():
    """ What occurs once the home route is called """
    fridge = Fridge_item.query.all()
    cupboard = Cupboard_item.query.all()
    return render_template("home.html", fridge=fridge, cupboard=cupboard)

#logged_in = False #this will be removed in time
#@app.route("/home")
#def home():
#    print(logged_in)
#    """ What occurs once the home route is called """
#    print("Rendering home...")
#    return render_template("home.html", fridge=fridge, cupboard=cupboard, logged_in=logged_in)


@app.route("/register", methods=['GET', 'POST'])
def register():
    """ What occues when the register route is called, a get request calls the render function and passes the register page template.
     page will redirect to home."""
    print("[" + str(datetime.datetime.now()) + "]" + "instanciating form...")
    form = RegistrationForm()
    if form.validate_on_submit():

        print("[" + str(datetime.datetime.now())+ "]" + "The form is valid!")
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_password, )
        db.session.add(user)
        db.session.commit()
        print("Account created!")
        return redirect(url_for('login'))
    return render_template('register.html', form=form)

@app.route("/login", methods=['GET', 'POST'])
def login():
    """ If a get request is submited the login page will be rendered. POST functionality yet to be implemented """
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)
            return redirect(url_for('home'))
    else:
        print("Login failed")
    return render_template('login.html', form=form)

@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))

@app.route("/account")
@login_required
def account():
    user = current_user
    form = ViewAccount(obj=user)
    return render_template('account.html', form=form)

@app.route("/add_to_fridge", methods=['GET','POST'])
@login_required
def add_to_fridge():
    form = AddToFridgeForm()
    if form.validate_on_submit():
        fridge_item = Fridge_item(item_name=form.item_name.data, quantity=form.quantity.data, use_by=form.use_by.data, image_file=form.image_file.data, owner=current_user.id)
        print(fridge_item)
        db.session.add(fridge_item)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_to_fridge.html', form=form)


@app.route("/add_to_cupboard", methods=['GET','POST'])
@login_required
def add_to_cupboard():
    form = AddToCupboardForm()
    if form.validate_on_submit():
        cupboard_item = Cupboard_item(item_name=form.item_name.data, quantity=form.quantity.data, image_file=form.image_file.data, owner=current_user.id)
        db.session.add(cupboard_item)
        db.session.commit()
        return redirect(url_for('home'))
    return render_template('add_to_cupboard.html', form=form)


#@app.route("/item/fridge/<int:fridge_item_id>")
#@login_required
#def fridge_item(fridge_item_id):
#    item = Fridge_item.query.get_or_404(fridge_item_id)
#    return render_template('fridge_item.html', item=item)

@app.route("/item/fridge/<int:fridge_item_id>", methods=['GET', 'POST'])
@login_required
def update_fridge_item(fridge_item_id):
    fridge_item = Fridge_item.query.get_or_404(fridge_item_id)
    #if fridge_item.owner != current_user:
     #   abort(403)

    form = FridgeItemForm()
    if form.validate_on_submit():
        fridge_item.item_name = form.item_name.data
        fridge_item.quantity = form.quantity.data
        fridge_item.use_by = form.use_by.data
        fridge_item.image_file = form.image_file.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.item_name.data = fridge_item.item_name
        form.quantity.data = fridge_item.quantity
        # form.use_by.data = fridge_item.use_by
        form.image_file.data = fridge_item.image_file
    return render_template('fridge_item.html', form=form )

@app.route("/item/cupboard/<int:cupboard_item_id>", methods=['GET', 'POST'])
@login_required
def update_cupboard_item(cupboard_item_id):
    cupboard_item = Cupboard_item.query.get_or_404(cupboard_item_id)
    #if fridge_item.owner != current_user:
     #   abort(403)

    form = CupboardItemForm()
    if form.validate_on_submit():
        cupboard_item.item_name = form.item_name.data
        cupboard_item.quantity = form.quantity.data
        cupboard_item.image_file = form.image_file.data
        db.session.commit()
        return redirect(url_for('home'))
    elif request.method == 'GET':
        form.item_name.data = cupboard_item.item_name
        form.quantity.data = cupboard_item.quantity
        # form.use_by.data = fridge_item.use_by
        form.image_file.data = cupboard_item.image_file
    return render_template('cupboard_item.html', form=form )

@app.route("/item/fridge/<int:fridge_item_id>/delete", methods=['GET','POST'])
@login_required
def delete_fridge_item(fridge_item_id):
    fridge_item = Fridge_item.query.get_or_404(fridge_item_id)
    db.session.delete(fridge_item)
    db.session.commit()
    return redirect(url_for('home'))

@app.route("/item/cupboard/<int:cupboard_item_id>/delete", methods=['GET','POST'])
@login_required
def delete_cupboard_item(cupboard_item_id):
    cupboard_item = Cupboard_item.query.get_or_404(cupboard_item_id)
    db.session.delete(cupboard_item)
    db.session.commit()
    return redirect(url_for('home'))    

@app.route("/whatsoff", methods=['GET'])
def whatsoff():
    payload = Fridge_item.query.all()
    iffy_items = watcher0.checkIffies(payload)
    off_items = watcher0.checkOffies(payload)
    return render_template('whatsoff.html', iffy=iffy_items, offy=off_items)

def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@login_required
@app.route('/reciptscan', methods=['GET', 'POST'])
def reciptscan():
    if request.method == 'POST':
        print("Posting...")
        # check if the post request has the file part
        if 'pic-file' not in request.files:
            print("No file in part")
            return redirect(url_for('reciptscan'))
        recipt = request.files['pic-file']
        print("Recipt img: " + str(recipt.filename))
        # if user does not select file, browser also
        # submit an empty part without filename
        if recipt.filename == '':
            print('No selected file')
            return redirect(url_for('reciptscan'))
        if recipt and allowed_file(recipt.filename):
            filename = secure_filename(recipt.filename)
            recipt.save(os.path.join(app.config['UPLOADED_PHOTOS_DEST'], filename))
            recipt.close()
            print("file is allowed: " + filename)
            return redirect(url_for('reciptscan',
                                    upload=filename))
    return render_template('reciptscan.html')

@app.context_processor
def utility_functions():
    def print_in_console(message):
        print(message)

    return dict(mdebug=print_in_console)

#@app.route("/reciptscan", methods=['GET', 'POST'])
#@login_required
#def reciptscan():
#    print(ALLOWED_EXTENSIONS)
#    if request.method == 'POST' and 'photo' in request.files:
#        filename = photos.save(request.files['photo'])
#        print("POST, contents of filename var: " + filename) 
#        return filename
#    return render_template('reciptscan.html')



