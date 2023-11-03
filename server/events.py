from .models import Event, EventStatus, Comment, Status, User
from flask import Blueprint, request, render_template, session, request, redirect, url_for, flash
from .models import Event, EventStatus, Comment, Status, TicketOrder
from .forms import EventForm, EventUpdateForm, CommentForm
from . import db
import os
from werkzeug.utils import secure_filename
from flask_login import login_required, current_user
from datetime import date, datetime

event_bp = Blueprint('event', __name__, url_prefix='/events')

# @event_bp.route('/<id>')
# def show(id):
#     event = db.session.scalar(db.select(Event).where(Event.id==id))
#     # create the comment form
#     form = CommentForm()    
#     return render_template('events/event-page.html', event=event, form=form)

def update_status():
	e = db.session.query(Event).filter(Event.date <= date.today())
	for ev in e:
		if(ev.date==date.today()):
			if(ev.time.strftime("%H:%M") >= datetime.now().strftime("%H:%M")):
				continue
			if(ev.status == Status.e):
				continue
		s = db.session.scalar(db.select(EventStatus).where(EventStatus.Event_id==ev.id))
		s.status = Status.e
	seat = db.session.query(Event).filter(Event.currentSeating==Event.maxSeating)
	for i in seat:
		k = db.session.scalar(db.select(EventStatus).where(EventStatus.Event_id==i.id))
		if((k.status==Status.e) or (k.status==Status.s)):
			continue
		k.status = Status.s
	db.session.commit()

def validate_date(d, t):
	if(d < date.today()):
		flash('Invalid date')
		return False
	if((d == date.today()) and (t.strftime("%H:%M") < datetime.now().strftime("%H:%M"))):
		flash('Invalid date')
		return False
	else:
		return True

@event_bp.route('/event_creation', methods=['GET', 'POST'])
@login_required
def event_creation():
	print('Method type: ', request.method)
	form = EventForm()
	if form.validate_on_submit():
		if (not validate_date(form.date.data, form.time.data)):
			return redirect(url_for('event.event_creation'))
		#call the function that checks and returns image
		db_file_path = check_upload_file(form)
		event = Event(creator_id=current_user.id, name=form.name.data, description=form.description.data, tags = form.tags.data,
							image=db_file_path, venue_name=form.venue_name.data, address=form.address.data, 
							ticket_cost=form.ticket_cost.data, artist=form.artist.data, date=form.date.data, time=form.time.data, 
							maxSeating=form.maxSeating.data, currentSeating=0)
		# add the object to the db session
		
		db.session.add(event)
		# commit to the database
		db.session.flush()
		stat = EventStatus(Event_id=event.id, status=Status.a)
		db.session.add(stat)
		db.session.commit()
		
		print('Successfully created new event', 'success')
		#Always end with redirect when form is valid
		return redirect(url_for('event.event_creation'))
	return render_template('events/event-creation.html', form=form)

@event_bp.route('/update_event/<id>', methods=['GET','POST'])
@login_required
def update_event(id):
	event = db.session.scalar(db.select(Event).where(Event.id==id))
	form = EventUpdateForm(obj=event)
	if form.validate_on_submit():
		if (not validate_date(form.date.data, form.time.data)):
			return redirect(url_for('event.load_created_events'))
		event.name = form.name.data
		event.artist = form.artist.data
		event.description = form.description.data
		event.tags = form.tags.data
		event.venue_name = form.venue_name.data
		event.ticket_cost = form.ticket_cost.data
		event.date = form.date.data
		event.time = form.time.data
		event.maxSeating = form.maxSeating.data
		if(form.image.data != event.image):
			event.image = check_upload_file(form)
		db.session.commit()
		return redirect(url_for('event.load_created_events'))
	return render_template('events/event-creation.html', form=form)

@event_bp.route('/my_events', methods=['GET'])
@login_required
def load_created_events():
	update_status()
	id=current_user.id
	events = db.session.query(Event).filter(Event.creator_id==id)
	
	return render_template('events/my_events.html', events = events)

@event_bp.route('/', methods=['GET'])
def load_events():
	update_status()
	events = db.session.scalars(db.select(Event))
	users = db.session.scalars(db.select(User))
	return render_template('events-browser.html', events = events, users = users)

@event_bp.route('/<id>', methods=['GET'])
def show(id):
	update_status()
	event = db.session.scalar(db.select(Event).where(Event.id==id))
    # create the comment form
	print(f'The ID: {id} \n')
	user = db.session.scalar(db.select(User).where(User.id==event.creator_id))
	form = CommentForm()    
	return render_template('events/event-page.html', event = event, form = form, user = user)

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

@event_bp.route('/bookings', methods=['GET'])
@login_required
def load_bookings():
	id=current_user.id
	ticket_order = db.session.scalar(db.select(TicketOrder).where(TicketOrder.id == id))
	events = db.session.scalar(db.select(Event).where(Event.id == ticket_order.event_id))

	return render_template('events/event-bookings.html', events = events)

@event_bp.route('/<id>/comment', methods=['GET', 'POST'])  
@login_required
def comment(id):  
    form = CommentForm()  
    #get the destination object associated to the page and the comment
    event = db.session.scalar(db.select(Event).where(Event.id==id))
    if form.validate_on_submit():  
      #read the comment from the form
      comment = Comment(text=form.text.data, event=event,
                        user=current_user) 
      #here the back-referencing works - comment.destination is set
      # and the link is created
      db.session.add(comment) 
      db.session.commit() 
      #flashing a message which needs to be handled by the html
      flash('Your comment has been added', 'success')  
      # print('Your comment has been added', 'success') 
    # using redirect sends a GET request to destination.show
    return redirect(url_for('event.show', id=id))