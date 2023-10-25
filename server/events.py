from flask import Blueprint, request, render_template, session, request, redirect, url_for
from .models import Event, EventStatus, Comment
from .forms import EventForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user

evbp = Blueprint('Event', __name__, url_prefix='/events')

@evbp.route('/eventcreation', methods=['GET', 'POST'])
@login_required
def eventcreation():
  print('Method type: ', request.method)
  form = EventForm()
  if form.validate_on_submit():
    #call the function that checks and returns image
    db_file_path = check_upload_file(form)
    event = Event(creator_id=current_user.id, name=form.name.data, description=form.description.data, 
                        image=db_file_path, venue_name=form.ven_name.data, address=form.address.data, 
                        ticket_cost=form.cost.data, artist=form.artist.data, date_time=form.date.data, 
                        maxSeating=form.capacity.data, currentSeating=0)
    # add the object to the db session
    db.session.add(event)
    # commit to the database
    db.session.flush()
    stat = EventStatus(Event_id=event.id, status='Active')
    db.session.add(stat)
    db.session.commit()
    
    print('Successfully created new travel destination', 'success')
    #Always end with redirect when form is valid
    return redirect(url_for('Event.eventcreation'))
  return render_template('events/eventcreation.html', form=form)


'''
@evbp.route('/<id>')
def show(id):
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
    cform = CommentForm()    
    return render_template('events/show.html', event=event, form=cform)
'''

def check_upload_file(form):
  #get file data from form  
  fp = form.image.data
  filename = fp.filename
  #get the current path of the module file… store image file relative to this path  
  BASE_PATH = os.path.dirname(__file__)
  #upload file location – directory of this file/static/image
  upload_path = os.path.join(BASE_PATH,'static/image',secure_filename(filename))
  #store relative path in DB as image location in HTML is relative
  db_upload_path = '/static/image/' + secure_filename(filename)
  #save the file and return the db upload path  
  fp.save(upload_path)
  return db_upload_path




