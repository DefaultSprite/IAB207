from collections.abc import Mapping, Sequence
from typing import Any
from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, DateField, TimeField, IntegerField, DecimalField, FieldList
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

#creates the login information
class LoginForm(FlaskForm):
    email=StringField("Email", validators=[InputRequired('Enter email'), Email("Please enter a valid email")])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

    # this is the registration form
class RegisterForm(FlaskForm):
    f_name=StringField("First Name", validators=[InputRequired()])
    l_name=StringField("Last Name", validators=[InputRequired()])
    p_number=StringField("Phone Number", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[InputRequired('Enter email'), Email("Please enter a valid email")])
        #linking two fields - password should be equal to data entered in confirm
    password=PasswordField("Password", validators=[InputRequired(),
                    EqualTo('confirm', message="Passwords should match"), Length(min=8)])
    confirm = PasswordField("Confirm Password")
        #submit button
    submit = SubmitField("Register")

ALLOWED_FILE = {'PNG', 'JPG', 'JPEG', 'png', 'jpg', 'jpeg'}

class EventForm(FlaskForm):
  name = StringField('Name of Event', validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the 
  #description meets the length requirements
  artist = StringField('Name of Artist/s', validators=[InputRequired()])
  description = TextAreaField('Description', validators = [InputRequired()])
  tags = TextAreaField('Add tags', validators=[InputRequired()])
  venue_name = StringField('Name of Venue', validators=[InputRequired()])
  address = StringField('Address of Venue', validators=[InputRequired()])
  ticket_cost = DecimalField('Cost of Ticket', validators=[InputRequired()])
  date = DateField('Date and Time of Event', validators=[InputRequired()])
  time = TimeField('Date and Time of Event',validators=[InputRequired()])
  maxSeating = IntegerField('Maximum Capacity of Venue', validators=[InputRequired()])
  image = FileField('Event Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
  submit = SubmitField("Create")

class EventUpdateForm(FlaskForm):
  name = StringField('Name of Event', validators=[InputRequired()])
  # adding two validators, one to ensure input is entered and other to check if the 
  #description meets the length requirements
  artist = StringField('Name of Artist/s', validators=[InputRequired()])
  description = TextAreaField('Description', validators = [InputRequired()])
  tags = TextAreaField('Add tags (e.g Rock, ACDC)', validators=[InputRequired()])
  venue_name = StringField('Name of Venue', validators=[InputRequired()])
  address = StringField('Address of Venue', validators=[InputRequired()])
  ticket_cost = DecimalField('Cost of Ticket', validators=[InputRequired()])
  date = DateField('Date and Time of Event', validators=[InputRequired()])
  time = TimeField('Date and Time of Event',validators=[InputRequired()])
  maxSeating = IntegerField('Maximum Capacity of Venue', validators=[InputRequired()])
  image = FileField('Event Image (do not need to add file if not changing image)', validators=[
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
  submit = SubmitField("Update")