from flask import Blueprint

import controllers

event = Blueprint('event', __name__)

@event.route('/event', methods=['POST'])
def create_event():
    return controllers.create_event()

@event.route('/events', methods=['GET'])
def get_all_events():
    return controllers.get_all_events()

@event.route('/event/<event_id>', methods=['GET'])
def get_event_by_id(event_id):
    return controllers.get_event_by_id(event_id)

@event.route('/event/<event_id>', methods=['PUT'])
def update_event_by_id(event_id):
    return controllers.update_event_by_id(event_id)

@event.route('/event/<event_id>/delete', methods=['DELETE'])
def delete_event_by_id(event_id):
    return controllers.delete_event_by_id(event_id)