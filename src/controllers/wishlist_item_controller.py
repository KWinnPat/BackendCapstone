from flask import jsonify, request
from db import db

from models.wishlist_item import WishlistItems, wishlist_item_schema, wishlist_items_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate
def create_wishlist_item():
    data = request.form if request.form else request.get_json()
    new_wishlist_item = WishlistItems.new_wishlist_item_obj()

    populate_object(new_wishlist_item, data)

    try:
        db.session.add(new_wishlist_item)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to create record"}), 400

    return jsonify({"message": "wishlist item created", "results": wishlist_item_schema.dump(new_wishlist_item)}), 201

#READ
@authenticate
def get_all_wishlist_items():
    query = db.session.query(WishlistItems).all()
    return jsonify({"results": wishlist_items_schema.dump(query)}), 200

@authenticate
def get_wishlist_item_by_id(wishlist_item_id):
    query = db.session.query(WishlistItems).filter(WishlistItems.wishlist_item_id == wishlist_item_id).first()
    if not query:
        return jsonify({"message": "wishlist item not found"}), 404
    return jsonify({"results": wishlist_item_schema.dump(query)}), 200

#UPDATE
@authenticate
def update_wishlist_item_by_id(wishlist_item_id):
    query = db.session.query(WishlistItems).filter(WishlistItems.wishlist_item_id == wishlist_item_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "wishlist item updated", "results": wishlist_item_schema.dump(query)}), 200

#DELETE
@authenticate
def delete_wishlist_item_by_id(wishlist_item_id):
    query = db.session.query(WishlistItems).filter(WishlistItems.wishlist_item_id == wishlist_item_id).first()

    if not query:
        return jsonify({"message": "wishlist item not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "wishlist item deleted"}), 200