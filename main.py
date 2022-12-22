from flask import Flask, render_template, request
from flask_sqlalchemy import SQLAlchemy



app = Flask(__name__)
app.config ['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///workout.db'
db = SQLAlchemy(app)
app.app_context().push()


class WorkoutData(db.Model):
   __tablename__ = "workoutdata"
   id = db.Column('id', db.Integer, primary_key = True)
   day = db.Column(db.String(250), nullable=False)
   muscle = db.Column(db.String(250), nullable=False)
   weight = db.Column(db.Integer, nullable=False)


#db.create_all()


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
if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
