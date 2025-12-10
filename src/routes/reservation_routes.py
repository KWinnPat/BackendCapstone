from flask import Blueprint

import controllers

reservation = Blueprint('reservation', __name__)

@reservation.route('/reservation', methods=['POST'])
def create_reservation():
    return controllers.create_reservation()

@reservation.route('/user/reservation', methods=['POST'])
def create_user_reservation():
    return controllers.create_user_reservation()

@reservation.route('/reservations', methods=['GET'])
def get_all_reservations():
    return controllers.get_all_reservations()

@reservation.route('/reservation/<reservation_id>', methods=['GET'])
def get_reservation_by_id(reservation_id):
    return controllers.get_reservation_by_id(reservation_id)

@reservation.route('/reservation/<reservation_id>', methods=['PUT'])
def update_reservation_by_id(reservation_id):
    return controllers.update_reservation_by_id(reservation_id)

@reservation.route('/reservation/<reservation_id>/delete', methods=['DELETE'])
def delete_reservation_by_id(reservation_id):
    return controllers.delete_reservation_by_id(reservation_id)

@reservation.route('/<user_id>/<reservation_id>/delete', methods=['DELETE'])
def delete_user_reservation(user_id, reservation_id):
    return controllers.delete_user_reservation(user_id, reservation_id)