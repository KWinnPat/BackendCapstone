from flask import Blueprint

import controllers

wishlist_item = Blueprint('wishlist_item', __name__)

@wishlist_item.route('/wishlist_item', methods=['POST'])
def create_wishlist_item():
    return controllers.create_wishlist_item()

@wishlist_item.route('/wishlist_items', methods=['GET'])
def get_all_wishlist_items():
    return controllers.get_all_wishlist_items()

@wishlist_item.route('/wishlist_item/<wishlist_item_id>', methods=['GET'])
def get_wishlist_item_by_id(wishlist_item_id):
    return controllers.get_wishlist_item_by_id(wishlist_item_id)

@wishlist_item.route('/wishlist_item/<wishlist_item_id>', methods=['PUT'])
def update_wishlist_item_by_id(wishlist_item_id):
    return controllers.update_wishlist_item_by_id(wishlist_item_id)

@wishlist_item.route('/wishlist_item/<wishlist_item_id>/delete', methods=['DELETE'])
def delete_wishlist_item_by_id(wishlist_item_id):
    return controllers.delete_wishlist_item_by_id(wishlist_item_id)