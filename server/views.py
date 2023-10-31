from flask import Blueprint, request, render_template, session,  redirect, url_for
from .models import Event
from . import db

main_bp = Blueprint('Main', __name__)

@main_bp.route('/')
def index() -> str:
    events = db.session.scalars(db.select(Event))
    return render_template('index.html', events = events)