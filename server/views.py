from flask import Blueprint, request, render_template, session,  redirect, url_for
from .models import Event
from . import db

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index() -> str:
    events = db.session.scalars(db.select(Event))
    return render_template('index.html', events = events)

@main_bp.route('/search')
def search():
    if request.args['search'] and request.args['search'] != "":
        print(request.args['search'])
        print("hello world")
        query = "%" + request.args['search'] + "%"
        events = db.session.query(Event).filter(Event.name.like(query))
        
        return render_template('events-browser.html', events=events)
    else:
        return redirect(url_for('main.index'))