import datetime
import re
from datetime import timedelta

def add_data(db, form):
    from app import User
    x_coordinate = form['leftPixel']
    y_coordinate = form['topPixel']
    building = form['Building'].lower()
    time = datetime.datetime.now()
    data = User(x_coordinate, y_coordinate, time, building)
    db.session.add(data)
    db.session.commit()
    placeholder = None
    return x_coordinate, y_coordinate, building, placeholder

def fetch_data(db, building, placeholder):
    from app import User
    x_coord = []
    y_coord = []
    users = db.session.query(User).filter(User.building == building)
    length = 0
    for user in users:
        user_time = user.time
        current_time = datetime.datetime.now()
        #database entries will delete after 8 hours (this can be easily changed)
        if (current_time - user_time) > timedelta(hours = 8):
            db.session.delete(user)
            db.session.commit()
        else:
            try:
                x_coord.append(int(float(user.x_coordinate)))
                y_coord.append(int(float(user.y_coordinate)))
                length+=1
            except ValueError:
                #delete entry
                db.session.delete(user)
                db.session.commit()
    length = int(length)
    return x_coord, y_coord, length
