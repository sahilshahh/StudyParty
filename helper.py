import datetime
import re
from datetime import timedelta

def add_data(db, form):
    from app import User
    x_coordinate = form['leftPixel']
    y_coordinate = form['topPixel']
    screen_x = form['screenWidth']
    screen_y = form['screenHeight']
    zoomLevel = form['zoomLevel']
    building = form['Building'].lower()
    time = datetime.datetime.now()
    data = User(x_coordinate, y_coordinate, screen_x, screen_y, zoomLevel, time, building)
    db.session.add(data)
    db.session.commit()
    placeholder = None
    return x_coordinate, y_coordinate, screen_x, screen_y, zoomLevel, building, placeholder

def fetch_data(db, building, placeholder):
    from app import User
    x_coord = []
    y_coord = []
    screen_xs = []
    screen_ys = []
    zoomLevels = []
    users = db.session.query(User).filter(User.building == building)
    length = 0
    for user in users:
        user_time = user.time
        current_time = datetime.datetime.now()
        #database entries will delete after 8 hours (this can be easily changed)
        if (current_time - user_time) > timedelta(hours = 1):
            db.session.delete(user)
            db.session.commit()
        else:
            try:
                x_coord.append((float(user.x_coordinate)))
                y_coord.append((float(user.y_coordinate)))
                screen_xs.append((float(user.screen_x)))
                screen_ys.append((float(user.screen_y)))
                zoomLevels.append((float(user.zoomlevel)))
                length+=1
            except ValueError:
                #delete entry
                db.session.delete(user)
                db.session.commit()
    length = int(length)
    return x_coord, y_coord, screen_xs, screen_ys, zoomLevels, length
