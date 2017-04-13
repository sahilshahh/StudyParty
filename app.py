from flask import Flask, render_template, request, session, redirect, url_for, flash
import datetime
from werkzeug import secure_filename
import os
from datetime import timedelta
from sqlalchemy.exc import IntegrityError
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.exc import IntegrityError
from flask_heroku import Heroku
from helper import add_data, fetch_data

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/studyparty'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:321884@localhost:5432/studyparty'
heroku = Heroku(app)
db = SQLAlchemy(app)
mypath = os.path.abspath(__file__)
mydir = os.path.dirname(mypath)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    x_coordinate = db.Column(db.String(120), unique=False) 
    y_coordinate = db.Column(db.String(120), unique=False)
    time = db.Column(db.DateTime, unique=False)
    building = db.Column(db.String(120), unique=False)


    def __init__(self, x_coordinate, y_coordinate, time, building):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.time = time
        self.building = building

    def __repr__(self):
        return '<Name %r>' % self.name

@app.route('/')
def home():
    buildings = []
    for name in os.listdir(os.path.join(mydir, "templates/building")):
        if name != 'template.html':
            buildings.append(name.split('.')[0])
    return render_template('home.html', buildings = buildings)

@app.route('/upload')
def upload():
    return render_template('upload.html')

@app.route('/uploading', methods=['POST'])
def uploading():
    if request.method == 'POST':
        uploaded_files = request.files.getlist("files")
        name = request.form['name'].lower()
        UPLOAD_FOLDER = os.path.join(mydir, 'static/img')
        app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
        for f in uploaded_files:
            file = secure_filename(f.filename)
            f.save(os.path.join(app.config['UPLOAD_FOLDER'], file))
            #now the variable file has the name of the file ie test.jpg and the name variable has the name of the building
            #now i have to create the two html files
            Html_file= open(os.path.join(mydir, 'templates/building/'+name+'*.html'),"w")
            Html_file.write(file)
            Html_file.close()

    return redirect(url_for('home'))

# Set "homepage" to index.html and fetches data for the heatmap
@app.route('/<building>')
def index(building):
    if '*' in building:
        Html_file= open(os.path.join(mydir, 'templates/building/'+building+'.html'),"r")
        image = Html_file.read() 
        x_coord, y_coord, length = fetch_data(db, building.lower(), placeholder = None)
        building_string = 'building/template.html'
        return render_template(building_string, x_coord=x_coord, y_coord=y_coord, length=length, building=building, image=image)
    else:
        x_coord, y_coord, length = fetch_data(db, building.lower(), placeholder = None)
        building_string = 'building/' + building.lower() + '.html'
        return render_template(building_string, x_coord=x_coord, y_coord=y_coord, length=length)

# Adds info to database and redirects to function that creats link
@app.route('/prereg', methods=['GET','POST'])
def prereg():
    if request.method == 'POST':
        x_coordinate, y_coordinate, building, placeholder = add_data(db, request.form)
        return redirect(url_for('map', building=building, x_coordinate=x_coordinate, y_coordinate=y_coordinate))
    else:
        return redirect(url_for('home'))

#generates the link for our map
@app.route('/map/<building>/<x_coordinate>/<y_coordinate>', methods=['GET','POST'])
def map(building, x_coordinate, y_coordinate):
    if request.method == 'GET':
        if '*' in building:
            Html_file= open(os.path.join(mydir, 'templates/building/'+building+'.html'),"r")
            image = Html_file.read() 
            building_string = 'buildingclick/templateclick.html'
            return render_template(building_string, x_coordinate=x_coordinate, y_coordinate=y_coordinate, building=building, image=image)
        else:    
            building_string = 'buildingclick/' + building.lower() + 'click.html'
            return render_template(building_string, x_coordinate=x_coordinate, y_coordinate=y_coordinate)
    else:
        return redirect(url_for('home'))

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()
