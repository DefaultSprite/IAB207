from . import db
from datetime import datetime
from flask_login import UserMixin
from sqlalchemy import Enum
import enum


class User(db.Model, UserMixin):
    __tablename__ = 'users' # good practice to specify table name
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), index=True, unique=True, nullable=False)
    emailid = db.Column(db.String(100), index=True, nullable=False)
	# password should never stored in the DB, an encrypted password is stored
	# the storage should be at least 255 chars long, depending on your hashing algorithm
    password_hash = db.Column(db.String(255), nullable=False)
    # relation to call user.comments and comment.created_by
    comments = db.relationship('Comment', backref='user')
    
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Events(db.Model):
    __tablename__ = 'Events'
    id = db.Column(db.Integer, primary_key=True)
    userID = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(80))
    venue_name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    artist = db.Column(db.String(80))
    date_time = db.Column(db.DateTime)
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    maxSeating = db.Column(db.Integer)
    currentSeating = db.Column(db.Integer)
    comments = db.relationship('Comment', backref='Events')
    status = db.relationship('Status', backref='Events')
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"


class Comment(db.Model):
    __tablename__ = 'comments'
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(400))
    created_at = db.Column(db.DateTime, default=datetime.now())
    # add the foreign key
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    destination_id = db.Column(db.Integer, db.ForeignKey('Events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"

class Status(enum.Enum):
    a = 'Active'
    c = 'Cancelled'
    e = 'Expired'


class EventStatus(db.Model):
    __tablename__ = 'EventStatus'
    id = db.Column(db.Integer, primary_key=True)
    Event_id = db.Column(db.Integer, db.ForeignKey('Events.id'))
    status = db.Column(Enum(Status))

    def __repr__(self):
        return f"Name: {self.status}"

class TicketOrder(db.Model):
    __tablename__= 'Order'
    id = db.Column(db.Integer, primary_key=True)
    ticketNum = db.Column(db.Integer)
    Event_id = db.Column(db.Integer, db.ForeignKey('Events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __repr__(self):
        return f"Name: {self.ticketNum}"
