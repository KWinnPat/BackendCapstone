from flask import jsonify, request
from db import db

from models.item import Items, item_schema, items_schema
from util.reflection import populate_object
from lib.authenticate import authenticate, authenticate_return_auth

#CREATE
@authenticate
def create_item():
    data = request.form if request.form else request.get_json()
    new_item = Items.new_item_obj()

    populate_object(new_item, data)

    try:
        db.session.add(new_item)
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        return jsonify({"message": "unable to create record", "error": str(e)}), 400
    
    return jsonify({"message": "item created", "results": item_schema.dump(new_item)}), 201
    

#READ
@authenticate
def get_all_items():
    query = db.session.query(Items).all()
    return jsonify({"results": items_schema.dump(query)}), 200

@authenticate
def get_item_by_id(item_id):
    query = db.session.query(Items).filter(Items.item_id == item_id).first()
    if not query:
        return jsonify({"message": "item not found"}), 404
    return jsonify({"results": item_schema.dump(query)}), 200

#UPDATE
@authenticate
def update_item_by_id(item_id):
    query = db.session.query(Items).filter(Items.item_id == item_id).first()
    data = request.form if request.form else request.get_json()

    populate_object(query, data)

    try:
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to update record"}), 400

    return jsonify({"message": "item updated", "results": item_schema.dump(query)}), 200

#DELETE
@authenticate
def delete_item_by_id(item_id):
    query = db.session.query(Items).filter(Items.item_id == item_id).first()

    if not query:
        return jsonify({"message": "item not found"}), 404

    try:
        db.session.delete(query)
        db.session.commit()
    except:
        db.session.rollback()
        return jsonify({"message": "unable to delete record"}), 400

    return jsonify({"message": "item deleted"}), 200