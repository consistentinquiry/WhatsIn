from flask_wtf import FlaskForm
from wtforms import IntegerField, StringField, PasswordField, SubmitField, BooleanField
from wtforms.fields.html5 import DateField, DateTimeField
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError
from whatsin.models import User
from datetime import date

class RegistrationForm(FlaskForm):
    """   """
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    confirm = PasswordField('Confirm password', validators=[DataRequired(), EqualTo('password')])
    
    key  = StringField('Access key', validators=[DataRequired(), Length(min=16, max=16)])


    submit = SubmitField('Sign up')

    def validate_username(self, username):
        user = User.query.filter_by(username=username.data).first()
        if user:
            raise ValidationError('Username is alreay taken')

    def validate_email(self, email):
        user = User.query.filter_by(email=email.data).first()
        if user:
            raise ValidationError('Email is alreay taken')

    def validate_key(self, key):
        if key.data != "psTu@92ZfgvOmiS*":
            raise ValidationError('Key not valid')

class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired(), Length(min=2, max=20)])
    password = PasswordField('Password', validators=[DataRequired()])
    remember = BooleanField('Remeber Me')
    login = SubmitField('Sign up')

class AddToFridgeForm(FlaskForm):
    item_name = StringField('Item name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    use_by = DateField('Use by', default=date.today )
    image_file = StringField('Image file', default="default.png")
    
    submit = SubmitField('Sign up')


class AddToCupboardForm(FlaskForm):
    item_name = StringField('Item name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    image_file = StringField('Image file', default="cupboard_default.png")

    submit = SubmitField('Sign up')

class FridgeItemForm(FlaskForm):
    item_name = StringField('Item name',  validators=[DataRequired()])
    quantity = IntegerField('Quantity',  validators=[DataRequired()])
    use_by = DateField('Use by' )
    image_file = StringField('Image file')

    submit = SubmitField('Sign up')

class CupboardItemForm(FlaskForm):
    item_name = StringField('Item name', validators=[DataRequired()])
    quantity = IntegerField('Quantity', validators=[DataRequired()])
    image_file = StringField('Image file')

    submit = SubmitField('Sign up')



