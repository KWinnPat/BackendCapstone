from flask import jsonify, request
from db import db

from models.event import Events, event_schema, events_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate
def create_event():
    data = request.form if request.form else request.get_json()
    new_event = Events.new_event_obj()

    populate_object(new_event, data)

    try:
        db.session.add(new_event)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "event created", "results": event_schema.dump(new_event)}), 201

#READ
@authenticate
def get_all_events():
    query = db.session.query(Events).all()
    return jsonify({"results": events_schema.dump(query)}), 200

@authenticate
def get_event_by_id(event_id):
    query = db.session.query(Events).filter(Events.event_id == event_id).first()
    if not query:
        return jsonify({"message": "event not found"}), 404
    return jsonify({"results": event_schema.dump(query)}), 200

#UPDATE
@authenticate_return_auth
def update_event_by_id(event_id, auth_info):
    query = db.session.query(Events).filter(Events.event_id == event_id).first()
    data = request.form if request.form else request.get_json()

    if auth_info.user.role == 'admin':
        
        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "event updated", "results": event_schema.dump(query)}), 200
    
    return jsonify({"message": "unauthorized"}), 401

#DELETE
@authenticate_return_auth
def delete_event_by_id(event_id, auth_info):
    query = db.session.query(Events).filter(Events.event_id == event_id).first()
    if auth_info.user.role == 'admin':
        if not query:
            return jsonify({"message": "event not found"}), 404
    
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400

        return jsonify({"message": "event deleted"}), 200
    
    return jsonify({"message": "unauthorized"}), 401