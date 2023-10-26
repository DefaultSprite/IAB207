from flask_wtf import FlaskForm
from wtforms.fields import TextAreaField,SubmitField, StringField, PasswordField, DateTimeField, IntegerField, DecimalField
from wtforms.validators import InputRequired, Length, Email, EqualTo
from flask_wtf.file import FileRequired, FileField, FileAllowed

#creates the login information
class LoginForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired('Enter user name')])
    password=PasswordField("Password", validators=[InputRequired('Enter user password')])
    submit = SubmitField("Login")

    # this is the registration form
class RegisterForm(FlaskForm):
    user_name=StringField("User Name", validators=[InputRequired()])
    email_id = StringField("Email Address", validators=[Email("Please enter a valid email")])
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
  venue_name = StringField('Name of Venue', validators=[InputRequired()])
  address = StringField('Address of Venue', validators=[InputRequired()])
  ticket_cost = DecimalField('Cost of Ticket', validators=[InputRequired()])
  date_time = DateTimeField('Date and Time of Event', 
                       validators=[InputRequired()], format='%Y-%m-%d %H:%M', 
                       render_kw={"placeholder":"yyyy-mm-dd hh:mm"})
  maxSeating = IntegerField('Maximum Capacity of Venue', validators=[InputRequired()])
  image = FileField('Destination Image', validators=[
    FileRequired(message = 'Image cannot be empty'),
    FileAllowed(ALLOWED_FILE, message='Only supports png, jpg, JPG, PNG')])
  submit = SubmitField("Create/Update")