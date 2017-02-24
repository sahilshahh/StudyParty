from flask import Flask, render_template, request, session, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_heroku import Heroku

app = Flask(__name__)
#app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/studyparty'
heroku = Heroku(app)
db = SQLAlchemy(app)

# Create our database model
class User(db.Model):
    __tablename__ = "users"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), unique=True)
    location = db.Column(db.String(120), unique=True)

    def __init__(self, name, location):
        self.name = name
        self.location = location

    def __repr__(self):
        return '<Name %r>' % self.name

# Set "homepage" to index.html
@app.route('/')
def index():
    return render_template('index.html')

# Save e-mail to database and send to success page
@app.route('/prereg', methods=['POST'])
def prereg():
    name = None
    if request.method == 'POST':
        name = request.form['name']
        location = request.form['location']
        # Check that name does not already exist (not a great query, but works)
        if not db.session.query(User).filter(User.name == name).count():
            reg = User(name, location)
            db.session.add(reg)
            db.session.commit()
            #session['name'] = name
            #session['location'] = location
            return redirect(url_for('map', location=location, name=name))
            #return render_template('success.html', name=name, location=location)
    return render_template('index.html')

@app.route('/map/<name>/<location>')
def map(location, name):
    return render_template('success.html', name=name, location=location)

if __name__ == '__main__':
    app.secret_key = 'super secret key'
    app.debug = True
    app.run()