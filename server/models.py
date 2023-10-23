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
    created_event = db.relationship('Event', backref='user')
    orders = db.relationship('TicketOrder', backref='user')
    
    # string print method
    def __repr__(self):
        return f"Name: {self.name}"

class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    creator_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    name = db.Column(db.String(80))
    description = db.Column(db.String(200))
    image = db.Column(db.String(400))
    venue_name = db.Column(db.String(80))
    address = db.Column(db.String(80))
    ticket_cost = db.Column(db.Double)
    artist = db.Column(db.String(80))
    date_time = db.Column(db.DateTime)
    maxSeating = db.Column(db.Integer)
    currentSeating = db.Column(db.Integer)
    # ... Create the Comments db.relationship
	# relation to call destination.comments and comment.destination
    comments = db.relationship('Comment', backref='event')
    orders = db.relationship('TicketOrder', backref='event')
    stat = db.relationship('EventStatus', backref='event')
	
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
    destination_id = db.Column(db.Integer, db.ForeignKey('events.id'))

    # string print method
    def __repr__(self):
        return f"Comment: {self.text}"
    
class TicketOrder(db.Model):
    __tablename__= 'Order'
    id = db.Column(db.Integer, primary_key=True)
    ticketNum = db.Column(db.Integer)
    Event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    def __repr__(self):
        return f"Name: {self.ticketNum}"

class Status(enum.Enum):
    a = 'Active'
    c = 'Cancelled'
    e = 'Expired'

class EventStatus(db.Model):
    __tablename__ = 'event_status'
    id = db.Column(db.Integer, primary_key=True)
    Event_id = db.Column(db.Integer, db.ForeignKey('events.id'))
    status = db.Column(Enum(Status))

    def __repr__(self):
        return f"Name: {self.status}"

