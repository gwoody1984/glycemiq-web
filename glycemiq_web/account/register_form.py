from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField
from wtforms.validators import DataRequired, Email, EqualTo


class RegisterForm(FlaskForm):
    email = StringField('Email address', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[
        DataRequired(), EqualTo('confirm', message='Passwords must match')])
    confirm = PasswordField('Re-enter Password', validators=[DataRequired()])
