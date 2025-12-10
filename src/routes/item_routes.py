from flask import Blueprint

import controllers

item = Blueprint('item', __name__)

@item.route('/item', methods=['POST'])
def create_item():
    return controllers.create_item()

@item.route('/items', methods=['GET'])
def get_all_items():
    return controllers.get_all_items()

@item.route('/item/<item_id>', methods=['GET'])
def get_item_by_id(item_id):
    return controllers.get_item_by_id(item_id)

@item.route('/item/<item_id>', methods=['PUT'])
def update_item_by_id(item_id):
    return controllers.update_item_by_id(item_id)

@item.route('/item/<item_id>/delete', methods=['DELETE'])
def delete_item_by_id(item_id):
    return controllers.delete_item_by_id(item_id)