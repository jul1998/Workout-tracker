from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class ContactForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField("Sign Me Up!")