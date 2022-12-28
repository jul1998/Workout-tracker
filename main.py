from flask import Flask, render_template, request, redirect, flash, url_for, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from forms import ContactForm, RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, UserMixin, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
import requests

login_manager = LoginManager()
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
app.config["SECRET_KEY"] = "MySecretKey"
db = SQLAlchemy(app)
app.app_context().push()
login_manager.init_app(app)
migreate = Migrate(app,db)

class WorkoutData(db.Model):
   __tablename__ = "workoutdata"
   id = db.Column('id', db.Integer, primary_key = True)
   day = db.Column(db.String(250), nullable=False)
   muscle = db.Column(db.String(250), nullable=False)
   weight = db.Column(db.Integer, nullable=False)

class Contacts(db.Model):
    __tablename__ = "contacts"
    id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(250), nullable=False)
    email = db.Column(db.String(250), nullable=False)
    message = db.Column(db.Text, nullable=False)


class User(UserMixin,db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String)
    email = db.Column(db.String)
    password = db.Column(db.String)

    def __repr__(self):
        return f"<User(name='{self.name}', email='{self.email}', password='{self.password}')>"

#db.create_all()
def show_cat_error(server_error):
    response = requests.get(url=f"https://http.cat/{server_error}")
    return response.url
@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)

@app.errorhandler(404)
def page_not_found(e):
    error_url = show_cat_error(404)
    return render_template("404.html", cat_error=error_url), 404
@app.errorhandler(401)
def page_not_authorized(e):
    error_url = show_cat_error(401)
    return render_template("401.html", cat_error=error_url), 401

@app.errorhandler(500)
def page_not_found(e):
    error_url = show_cat_error(500)
    return render_template("500.html", cat_error=error_url ), 500


@app.route("/")
def index():
    name = None
    if current_user.is_authenticated:
        name = current_user.username
    return render_template("index.html",
                           is_logged=current_user.is_authenticated,
                           name=name)

@app.route('/user_signup', methods=['GET', 'POST'])
def signup():
    registration_form = RegistrationForm()
    if registration_form.validate_on_submit():
        username = registration_form.username.data
        email = registration_form.email.data
        password = registration_form.password.data

        user = User.query.filter_by(email=email).first()
        if not user:
            hashed_password = generate_password_hash(password)
            new_user = User(username=username, email=email, password=hashed_password)
            db.session.add(new_user)
            db.session.commit()
            flash("Registration was successful")
            return redirect("/")#This has to change to login
        else:
            flash("user already exists")
            return redirect("/")#This has to change to login and flash message has to be red
    return render_template("signup.html", form=registration_form)

@app.route("/login", methods=["GET", "POST"])
def loging_page():
    login_form = LoginForm()
    if login_form.validate_on_submit():
        email = login_form.email.data
        password = login_form.password.data
        try:
            user = User.query.filter_by(email=email).first()
            print(user.email)
        except:
            flash("User does not exist")
            return redirect(url_for("loging_page"))
        else:
            if user:
                if check_password_hash(user.password, password):
                    login_user(user)
                    flash("Login successfully")
                    print(user.is_authenticated)
                    return redirect(url_for("index"))
                else:
                    flash("Password or user does not match")
                    return redirect(url_for("loging_page"))

    return render_template("login.html", form=login_form)

@app.route("/logout")
@login_required
def logout_page():
    logout_user()
    flash("User logout")
    return redirect(url_for("index"))


@app.route("/workout_data", methods=["GET", "POST"])
@login_required
def save_data():
    if request.method == "POST":
        days = request.form.get('days')
        muscles = request.form.get('muscles')
        weight = request.form.get("weight")
        new_data = WorkoutData(day=days, muscle=muscles, weight=weight)
        db.session.add(new_data)
        db.session.commit()

    return render_template("workout_data.html")

@app.route("/workout_trainer")
def search_trainer():
    return render_template("test_trainers.html")

@app.route("/contact_form", methods=["GET","POST"])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        form_email = contact_form.email.data
        form_name =  contact_form.email.name
        form_msg = contact_form.message.data
        new_contact = Contacts(email=form_email, name=form_name, message=form_msg )
        db.session.add(new_contact)
        db.session.commit()
        flash("Message sent successfully")
        return redirect ("/")
    return render_template("contact.html", form=contact_form)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
