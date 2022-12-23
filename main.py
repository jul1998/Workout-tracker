from flask import Flask, render_template, request, redirect
from flask_sqlalchemy import SQLAlchemy
from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired
from forms import ContactForm



app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
app.config["SECRET_KEY"] = "MySecretKey"
db = SQLAlchemy(app)
app.app_context().push()


class WorkoutData(db.Model):
   __tablename__ = "workoutdata"
   id = db.Column('id', db.Integer, primary_key = True)
   day = db.Column(db.String(250), nullable=False)
   muscle = db.Column(db.String(250), nullable=False)
   weight = db.Column(db.Integer, nullable=False)


#db.create_all()


@app.errorhandler(404)
def page_not_found(e):
    return render_template("404.html"), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template("404.html"), 500




@app.route("/")
def index():

    return render_template("index.html")

@app.route("/workout_data", methods=["GET", "POST"])
def save_data():
    if request.method == "POST":
        print("here")
        days = request.form.get('days')
        muscles = request.form.get('muscles')
        weight = request.form.get("weight")
        print(weight)
        new_data = WorkoutData(day=days, muscle=muscles, weight=weight)
        db.session.add(new_data)
        db.session.commit()

    return render_template("workout_data.html")

@app.route("/workout_trainer")
def search_trainer():
    return render_template("search_trainer.html")

@app.route("/contact_form", methods=["GET","POST"])
def contact():
    contact_form = ContactForm()
    if contact_form.validate_on_submit():
        print(contact_form.email.data)
        return redirect ("/")
    return render_template("contact.html", form=contact_form)



if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
