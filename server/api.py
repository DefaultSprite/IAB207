from flask import Blueprint, jsonify, request
from models import Event, Room
from . import db

api_bp = Blueprint('api', __name__, url_prefix='/api')

@api_bp.route('/events')
def get_hotel():
    events = db.session.scalars(db.select(Event)).all()
    event_list = [e.to_dict() for e in events]
    return jsonify(hotels=event_list)

@api_bp.route('/events', methods=['POST'])
def create_event():
    json_dict = request.get_json()
    if not json_dict:
        return jsonify(message="No input data provided!"), 400
    event = Event(name=json_dict['name'], description=json_dict['description'],
        destination_id=json_dict['event_id'])
    for room_json in json_dict['rooms']:
        if "event_id" in room_json:
            room = db.session.scalar(db.select(Room).where(Room.id==room_json.id))
        else:
            room = Room(type=room_json['room_type'], num_rooms=room_json['num_rooms'],
                description=room_json['room_description'], rate=room_json['room_rate'],
                hotel_id=event.id)
    db.session.add(event, room)
    db.session.commit()
    return jsonify(message='Successfully created new hotel!'), 201

@api_bp.route('/events/<int:hotel_id>', methods=['DELETE'])
def delete_event(hotel_id):
    hotel = db.session.scalar(db.select(Event).where(Event.id==hotel_id))
    db.session.delete(hotel)
    db.session.commit()
    return jsonify(message='Record deleted!'), 200

@api_bp.route('/events/<int:hotel_id>', methods=['PUT'])
def update_hotel(hotel_id):
    json_dict = request.get_json()
    hotel = db.session.scalar(db.select(Event).where(Event.id==hotel_id))
    hotel.name = json_dict['name']
    hotel.description = json_dict['description']
    db.session.commit()
    return jsonify(message='Record updated!'), 200