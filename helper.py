import datetime
from datetime import timedelta

def add_data(db, form):
    from app import User
    x_coordinate = form['leftPixel']
    y_coordinate = form['topPixel']
    time = datetime.datetime.now()
    data = User(x_coordinate, y_coordinate, time)
    db.session.add(data)
    db.session.commit()
    return x_coordinate,y_coordinate

def fetch_data(db):
    from app import User
    x_coord = []
    y_coord = []
    users = db.session.query(User)
    length = 0
    for user in users:
        user_time = user.time
        current_time = datetime.datetime.now()
        #database entries will delete after 12 hours (this can be easily changed)
        if (current_time - user_time) > timedelta(hours = 12):
            db.session.delete(user)
            db.session.commit()
        else:
            x_coord.append(int(float(user.x_coordinate)))
            y_coord.append(int(float(user.y_coordinate)))
            length+=1
    length = int(length)
    return x_coord, y_coord, length
