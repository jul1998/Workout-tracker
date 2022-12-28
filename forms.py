from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, EmailField, TextAreaField
from wtforms.validators import DataRequired, Length, EqualTo

class ContactForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Send Message')

class RegistrationForm(FlaskForm):
  username = StringField('Name', validators=[DataRequired()])
  email = EmailField('Email', validators=[])
  password = PasswordField('Password', validators=[
        Length(min=4, max=10),
        EqualTo('confirm_password', message='Passwords must match')])

  confirm_password = PasswordField('Password', validators=[DataRequired()])
  submit = SubmitField('Sign me up!')

class LoginForm(FlaskForm):
    email = EmailField('Email', validators=[Length(min=4, max=25)])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')
