from datetime import datetime
from werkzeug.security import generate_password_hash, check_password_hash
from flask.ext.admin.contrib.sqla import ModelView

from routeless.extensions import db, admin

class User(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    events = db.relationship('Event', backref='user', lazy='dynamic')
    courses = db.relationship('Course', backref='creator', lazy='dynamic')
    username = db.Column(db.String(64), unique=True)
    email = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    
    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
    
    def hash_password(self, password):
        self.password_hash = generate_password_hash(password)
        
    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)
        
        
class Course(db.Model):
    __tablename__ = 'course'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    check_points = db.relationship('CheckPoint', backref='course', lazy='dynamic')
    centerlat = db.Column(db.Float)
    centerlon = db.Column(db.Float)
    map_layer = db.Column(db.String(10))
    zoom = db.Column(db.Integer)
    date_created = db.Column(db.DateTime(), default=datetime.utcnow)
    date_edited = db.Column(db.DateTime(), default=datetime.utcnow)
    description = db.Column(db.Text())


class Event(db.Model):
    __tablename__ = 'event'
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    routes = db.relationship('Route', backref='event', lazy='dynamic')
    check_point_logs = db.relationship('CheckPointLog', backref='event', lazy='dynamic')
    date = db.Column(db.DateTime(), default=datetime.utcnow)
    time_elapsed = db.Column(db.Interval())


class CheckPoint(db.Model):
    __tablename__ = 'check_point'
    id = db.Column(db.Integer, primary_key=True)
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'))
    check_point_logs = db.relationship('CheckPointLog', backref='check_point', lazy='dynamic')
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    title = db.Column(db.String(10))
    description = db.Column(db.String(140))


class CheckPointLog(db.Model):
    __tablename__ = 'check_point_log'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    check_point_id = db.Column(db.Integer, db.ForeignKey('check_point.id'))
    log_points = db.relationship('LogPoint', backref='check_point_log', lazy='dynamic')
    found = db.Column(db.Integer)
    check_count = db.Column(db.Integer)


class Route(db.Model):
    __tablename__ = 'route'
    id = db.Column(db.Integer, primary_key=True)
    event_id = db.Column(db.Integer, db.ForeignKey('event.id'))
    route_points = db.relationship('RoutePoint', backref='route', lazy='dynamic')


class RoutePoint(db.Model):
    __tablename__ = 'route_point'
    id = db.Column(db.Integer, primary_key=True)
    route_id = db.Column(db.Integer, db.ForeignKey('route.id'))
    time = db.Column(db.DateTime(), default=datetime.utcnow)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)


class LogPoint(db.Model):
    __tablename__ = 'log_point'
    id = db.Column(db.Integer, primary_key=True)
    check_point_log_id = db.Column(db.Integer, db.ForeignKey('check_point_log.id'))
    time = db.Column(db.DateTime(), default=datetime.utcnow)
    lat = db.Column(db.Float)
    lon = db.Column(db.Float)
    type = db.Column(db.String(10))

admin.add_view(ModelView(User, db.session))