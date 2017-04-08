from flask import Flask, render_template, request, session, redirect, url_for, flash
import datetime
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku
from helper import add_data, fetch_data

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/studyparty'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:321884@localhost:5432/studyparty'
heroku = Heroku(app)
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    x_coordinate = db.Column(db.String(120), unique=True) 
    y_coordinate = db.Column(db.String(120), unique=True)
    time = db.Column(db.DateTime, unique=True)

    def __init__(self, x_coordinate, y_coordinate, time):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.time = time

    def __repr__(self):
        return '<Name %r>' % self.name

# Set "homepage" to index.html and fetches data for the heatmap
@app.route('/')
def index():
    x_coord, y_coord, length = fetch_data(db, placeholder = None)
    #x_coord = []
    #y_coord = []
    #users = db.session.query(User)
    #length = 0
    #for user in users:
        #user_time = user.time
        #current_time = datetime.datetime.now()
        #database entries will delete after 12 hours (this can be easily changed)
        #if (current_time - user_time) > timedelta(hours = 12):
            #db.session.delete(user)
            #db.session.commit()
        #else:
            #x_coord.append(int(float(user.x_coordinate)))
            #y_coord.append(int(float(user.y_coordinate)))
            #length+=1
    #length = int(length)
    return render_template('demo.html', x_coord=x_coord, y_coord=y_coord, length=length)

# Adds info to database and redirects to function that creats link
@app.route('/prereg', methods=['GET','POST'])
def prereg():
    if request.method == 'POST':
        x_coordinate, y_coordinate, placeholder = add_data(db, request.form)
        #x_coordinate = request.form['leftPixel']
        #y_coordinate = request.form['topPixel']
        #time = datetime.datetime.now()
        #reg = User(x_coordinate, y_coordinate, time)
        #db.session.add(reg)
        #db.session.commit()
        return redirect(url_for('map', x_coordinate=x_coordinate, y_coordinate=y_coordinate))
    else:
        return redirect(url_for('index'))

#generates the link for our map
@app.route('/map/<x_coordinate>/<y_coordinate>', methods=['GET','POST'])
def map(x_coordinate, y_coordinate):
    if request.method == 'GET':
        return render_template('democlick.html', x_coordinate=x_coordinate, y_coordinate=y_coordinate)
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()
