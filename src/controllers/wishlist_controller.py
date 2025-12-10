from flask import jsonify, request
from db import db

from models.wishlist import Wishlists, wishlist_schema, wishlists_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate
def create_wishlist():
    data = request.form if request.form else request.get_json()
    new_wishlist = Wishlists.new_wishlist_obj()

    populate_object(new_wishlist, data)

    try:
        db.session.add(new_wishlist)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "wishlist created", "results": wishlist_schema.dump(new_wishlist)}), 201

#READ
@authenticate_return_auth
def get_all_wishlists(auth_info):
    if auth_info.user.role == 'admin':
        query = db.session.query(Wishlists).all()
        return jsonify({"results": wishlists_schema.dump(query)}), 200
    
    return jsonify({"message": "unauthorized"}), 401

@authenticate
def get_wishlist_by_id(wishlist_id):
    query = db.session.query(Wishlists).filter(Wishlists.wishlist_id == wishlist_id).first()
    if not query:
        return jsonify({"message": "wishlist not found"}), 404
    return jsonify({"results": wishlist_schema.dump(query)}), 200

#UPDATE
@authenticate_return_auth
def update_wishlist_by_id(wishlist_id, auth_info):
    query = db.session.query(Wishlists).filter(Wishlists.wishlist_id == wishlist_id).first()
    data = request.form if request.form else request.get_json()

    if auth_info.user.role == 'admin' or query.user_id == str(auth_info.user.user_id):

        populate_object(query, data)

        try:
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to update record"}), 400

        return jsonify({"message": "wishlist updated", "results": wishlist_schema.dump(query)}), 200
    
    return jsonify({"message": "unauthorized"}), 401

#DELETE
@authenticate_return_auth
def delete_wishlist_by_id(wishlist_id, auth_info):
    query = db.session.query(Wishlists).filter(Wishlists.wishlist_id == wishlist_id).first()

    if auth_info.user.role == 'admin' or query.user_id == str(auth_info.user.user_id):
        if not query:
            return jsonify({"message": "wishlist not found"}), 404

        try:
            db.session.delete(query)
            db.session.commit()
        except:
            db.session.rollback()
            return jsonify({"message": "unable to delete record"}), 400

        return jsonify({"message": "wishlist deleted"}), 200
    
    return jsonify({"message": "unauthorized"}), 401