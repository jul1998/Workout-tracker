import random
from functools import wraps
from flask import Flask, render_template, request, redirect, flash, url_for, jsonify, wrappers, abort
from flask_sqlalchemy import SQLAlchemy
from forms import ContactForm, RegistrationForm, LoginForm
from flask_login import LoginManager, login_user, UserMixin, logout_user, current_user, login_required
from werkzeug.security import generate_password_hash, check_password_hash
from flask_migrate import Migrate
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
import requests
from dotenv import load_dotenv
import stripe
import os
load_dotenv()

stripe_keys = {
    'secret_key': 'sk_test_51MMFUJKfEnDDTBrd4iPHVPzlMhSzrCEzl3Vpd83qx33PzwsYE0WCsEhCdCHKwulRonvFC9bkAh71lvBUEem8XuaL00jQpDURgV',
    'publishable_key': 'pk_test_51MMFUJKfEnDDTBrdRNmeAGId82Y4pcf6kNXHxRw7HTb1m6GpysbuN7bi9H69DdaL3odyOaHCi0AiDfJhxilLuH3100US8REtD1'
}

stripe.api_key = stripe_keys['secret_key']

# website example https://www.strengthlog.com/exercise-directory/
login_manager = LoginManager()
app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
app.config["SECRET_KEY"] = os.getenv("SECRET_KEY")
db = SQLAlchemy(app)
app.app_context().push()
login_manager.init_app(app)
migreate = Migrate(app,db)

app.config['FLASK_ADMIN_SWATCH'] = 'cerulean'
admin = Admin(app, name='WorkoutPageAdmin', template_mode='bootstrap3')

#*--------------------------------------Models----------------------------
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


#*--------------------------------------Admin views----------------------------

admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Contacts, db.session))
admin.add_view(ModelView(WorkoutData, db.session))

#db.drop_all()
#db.create_all()

#*--------------------------------------login user----------------------------

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


def admin_only(func):
    @wraps(func)
    def wrapper(*args,**kwargs):
        try:
            if current_user.id != 1:
                return abort(403)

        except TypeError or AttributeError:
            pass
        else:
            return func(*args, **kwargs)
    return wrapper


#*--------------------------------------Handle Errors----------------------------

def show_cat_error(server_error):
    response = requests.get(url=f"https://http.cat/{server_error}")
    return response.url
@app.errorhandler(404)
def page_not_found(e):
    error_url = show_cat_error(404)
    return render_template("404.html", cat_error=error_url), 404
@app.errorhandler(401)
def page_not_authorized(e):
    error_url = show_cat_error(401)
    return render_template("401.html", cat_error=error_url), 401

@app.errorhandler(403)
def page_not_found(e):
    error_url = show_cat_error(403)
    return render_template("403.html", cat_error=error_url), 403
@app.errorhandler(500)
def page_not_found(e):
    error_url = show_cat_error(500)
    return render_template("500.html", cat_error=error_url ), 500

#*--------------------------------------Routes----------------------------
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

    return render_template("workout_data.html",  is_logged=current_user.is_authenticated)

@app.route("/workout_trainer")
@admin_only
@login_required
def search_trainer():
    return render_template("test_trainers.html",  is_logged=current_user.is_authenticated)

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
    return render_template("contact.html", form=contact_form,  is_logged=current_user.is_authenticated)

@app.route("/generate_random_exercises")
def random_exercises():
    response = requests.get("https://api.npoint.io/5deec383d686ac3c0486")
    all_data = response.json()
    random_exercise_to_display = all_data[random.randint(0, len(all_data) - 1)]
    return render_template("random_exercises.html", exercise_data=random_exercise_to_display, is_logged=current_user.is_authenticated)

@app.route("/charge", methods=["GET","POST"])
def make_charge():
    amount = 500


    publishable = stripe_keys['publishable_key']
    if request.method == "POST":
        customer = stripe.Customer.create(
            email='customer@example.com',
            source=request.form['stripeToken']
        )

        charge = stripe.Charge.create(
            customer=customer.id,
            amount=amount,
            currency='usd',
            description='Flask Charge'
        )

    # charge = stripe.Charge.retrieve(
    #     "ch_3MMFZKKfEnDDTBrd1y80HTfS",
    #     api_key="sk_test_51MMFUJKfEnDDTBrd4iPHVPzlMhSzrCEzl3Vpd83qx33PzwsYE0WCsEhCdCHKwulRonvFC9bkAh71lvBUEem8XuaL00jQpDURgV"
    # )
    #charge.capture()

    return render_template("paymentStripe.html", key=publishable)




if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
