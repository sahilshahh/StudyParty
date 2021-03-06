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
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/studyparty1'
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:321884@localhost:5432/studyparty'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = True
app.config['SECRET_KEY'] = 'hard to guess string'
heroku = Heroku(app)
db = SQLAlchemy(app)
mypath = os.path.abspath(__file__)
mydir = os.path.dirname(mypath)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    x_coordinate = db.Column(db.Float(), unique=False) 
    y_coordinate = db.Column(db.Float(), unique=False)
    screen_x = db.Column(db.Float(), unique=False)
    screen_y = db.Column(db.Float(), unique=False)
    zoomlevel = db.Column(db.Float(), unique=False)
    time = db.Column(db.DateTime, unique=False)
    building = db.Column(db.String(120), unique=False)


    def __init__(self, x_coordinate, y_coordinate, screen_x, screen_y, zoomlevel, time, building):
        self.x_coordinate = x_coordinate
        self.y_coordinate = y_coordinate
        self.screen_x = screen_x
        self.screen_y = screen_y
        self.zoomlevel = zoomlevel
        self.time = time
        self.building = building

    def __repr__(self):
        return '<Name %r>' % self.name

def building_list():
    buildings = []
    for name in os.listdir(os.path.join(mydir, "templates/building")):
        print(name[:-5])
        if name[:-5] != 'template':
            buildings.append(name[:-5].replace(' ', ''))
    print(buildings)
    return buildings

@app.route('/')
def home():
    #buildings = building_list()
    #return render_template('home.html', buildings = buildings)
    session['flag'] = False
    session['url'] = ''
    return redirect(url_for('index', building='fac'))

@app.route('/upload')
def upload():
    buildings = building_list()
    return render_template('upload.html', buildings=buildings)

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

    return redirect(url_for('index', building = name+'*'))

# Set "homepage" to index.html and fetches data for the heatmap
@app.route('/<building>')
def index(building):
    buildings = building_list()
    flag = session.get('flag')
    url = session.get('url')
    session['flag'] = False
    session['url'] = ''
    print(building)
    if '*' in building:
        Html_file= open(os.path.join(mydir, 'templates/building/'+building+'.html'),"r")
        image = Html_file.read() 
        x_coord, y_coord, screen_xs, screen_ys, zoomLevels, length = fetch_data(db, building.lower(), placeholder = None)
        building_string = 'building/template.html'
        return render_template(building_string, x_coord=x_coord, y_coord=y_coord, screen_xs=screen_xs, screen_ys=screen_ys, zoomLevels=zoomLevels, length=length, building=building, image=image, buildings = buildings, flag = flag, url=url)
    else:
        x_coord, y_coord, screen_xs, screen_ys, zoomLevels, length = fetch_data(db, building.lower(), placeholder = None)
        building_string = 'building/' + building.lower() + '.html'
        return render_template(building_string, x_coord=x_coord, y_coord=y_coord, screen_xs=screen_xs, screen_ys=screen_ys, zoomLevels=zoomLevels, length=length, buildings = buildings, flag = flag, url=url)

# Adds info to database and redirects to function that creats link
@app.route('/prereg', methods=['GET','POST'])
def prereg():
    if request.method == 'POST':
        x_coordinate, y_coordinate, screen_x, screen_y, zoomLevel, building, placeholder = add_data(db, request.form)
        session['flag'] = True
        session['url'] = 'https://study-party-ut.herokuapp.com/map/'+building+'/'+x_coordinate+'/'+y_coordinate+'/'+screen_x+'/'+screen_y+'/'+zoomLevel
        return redirect(url_for('index', building=building))
        #return redirect(url_for('map', building=building, x_coordinate=x_coordinate, y_coordinate=y_coordinate, screen_x=screen_x, screen_y=screen_y, zoomLevel=zoomLevel))
    else:
        return redirect(url_for('home'))

#generates the link for our map
@app.route('/map/<building>/<x_coordinate>/<y_coordinate>/<screen_x>/<screen_y>/<zoomLevel>', methods=['GET','POST'])
def map(building, x_coordinate, y_coordinate, screen_x, screen_y, zoomLevel):
    buildings = building_list()
    if request.method == 'GET':
        if '*' in building:
            Html_file= open(os.path.join(mydir, 'templates/building/'+building+'.html'),"r")
            image = Html_file.read() 
            building_string = 'buildingclick/templateclick.html'
            return render_template(building_string, x_coordinate=x_coordinate, y_coordinate=y_coordinate, screen_x=screen_x, screen_y=screen_y, zoomLevel=zoomLevel, building=building, image=image, buildings = buildings)
        else:    
            building_string = 'buildingclick/' + building.lower() + 'click.html'
            return render_template(building_string, x_coordinate=x_coordinate, y_coordinate=y_coordinate, screen_x=screen_x, screen_y=screen_y, zoomLevel=zoomLevel, buildings = buildings)
    else:
        return redirect(url_for('home'))

@app.route('/testing')
def testing():
    uploaded_buildings = []
    buildings = building_list()
    for building in buildings:
        if '*' in building:
            uploaded_buildings.append(building)
    return render_template('testing.html', buildings = uploaded_buildings)

@app.route('/upload_test', methods=['POST'])
def upload_test():
    building = request.form['building']
    #print(building)
    Html_file= open(os.path.join(mydir, 'templates/building/'+building+'.html'),"r")
    image = Html_file.read()
    #print(image) 
    os.remove(os.path.join(mydir, 'static/img/'+image))
    os.remove(os.path.join(mydir, 'templates/building/'+building+'.html'))
    return redirect(url_for('index', building='fac'))

@app.route('/database_test', methods=['POST'])
def database_test():
    x_coordinate, y_coordinate, screen_x, screen_y, zoomLevel, building, placeholder = add_data(db, request.form)
    return redirect(url_for('map', building=building, x_coordinate=x_coordinate, y_coordinate=y_coordinate, screen_x=screen_x, screen_y=screen_y, zoomLevel=zoomLevel))

if __name__ == '__main__':
    app.secret_key = 'hard to guess string'
    app.debug = True
    app.run()
