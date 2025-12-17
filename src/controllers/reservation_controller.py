from flask import jsonify, request
from db import db

from models.reservation import Reservations, reservation_schema, reservations_schema
from models.user import Users
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate
def create_reservation():
    data = request.form if request.form else request.get_json()
    new_reservation = Reservations.new_reservation_obj()

    populate_object(new_reservation, data)

    try:
        db.session.add(new_reservation)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to create record", "error": str(e)}), 400

    return jsonify({"message": "reservation created", "results": reservation_schema.dump(new_reservation)}), 201

@authenticate
def create_user_reservation():
    post_data = request.form if request.form else request.get_json()
    
    user = post_data.get('user_id')
    reservation_id = post_data.get('reservation_id')

    user = db.session.query(Users).filter(Users.user_id == user).first()
    reservation = db.session.query(Reservations).filter(Reservations.reservation_id == reservation_id).first()
    if not user or not reservation:
        return jsonify({"message": "user or reservation not found"}), 404
    reservation.user.append(user)
    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create association"}), 400
    return jsonify({"message": "user added to reservation", "results": reservation_schema.dump(reservation)}), 201

#READ
@authenticate
def get_all_reservations():
    query = db.session.query(Reservations).all()
    return jsonify({"results": reservations_schema.dump(query)}), 200

@authenticate
def get_reservation_by_id(reservation_id):
    query = db.session.query(Reservations).filter(Reservations.reservation_id == reservation_id).first()
    if not query:
        return jsonify({"message": "reservation not found"}), 404
    return jsonify({"results": reservation_schema.dump(query)}), 200

#UPDATE
@authenticate_return_auth
def update_reservation_by_id(reservation_id, auth_info):
    query = db.session.query(Reservations).filter(Reservations.reservation_id == reservation_id).first()
    data = request.form if request.form else request.get_json()

    if auth_info.user.role == 'admin':

        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "reservation updated", "results": reservation_schema.dump(query)}), 200
    
    return jsonify({"message": "unauthorized"}), 401

#DELETE
@authenticate_return_auth
def delete_reservation_by_id(reservation_id, auth_info):
    query = db.session.query(Reservations).filter(Reservations.reservation_id == reservation_id).first()
    if auth_info.user.role == 'admin':
        if not query:
            return jsonify({"message": "reservation not found"}), 404
    
        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400

        return jsonify({"message": "reservation deleted"}), 200
    
    return jsonify({"message": "unauthorized"}), 401

@authenticate_return_auth
def delete_user_reservation(user_id, reservation_id, auth_info):
    reservation = db.session.query(Reservations).filter(Reservations.reservation_id == reservation_id).first()
    user = db.session.query(Users).filter(Users.user_id == user_id).first()
    if not reservation or not user:
        return jsonify({"message": "user or reservation not found"}), 404

    if auth_info.user.role == 'admin' or str(auth_info.user.user_id) == str(user_id):
        if user in reservation.user:
            reservation.user.remove(user)
        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete association"}), 400
        return jsonify({"message": "user removed from reservation", "results": reservation_schema.dump(reservation)}), 200

    return jsonify({"message": "unauthorized"}), 401