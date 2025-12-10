from flask import Blueprint

import controllers

wishlist = Blueprint('wishlist', __name__)

@wishlist.route('/wishlist', methods=['POST'])
def create_wishlist():
    return controllers.create_wishlist()

@wishlist.route('/wishlists', methods=['GET'])
def get_all_wishlists():
    return controllers.get_all_wishlists()

@wishlist.route('/wishlist/<wishlist_id>', methods=['GET'])
def get_wishlist_by_id(wishlist_id):
    return controllers.get_wishlist_by_id(wishlist_id)

@wishlist.route('/wishlist/<wishlist_id>', methods=['PUT'])
def update_wishlist_by_id(wishlist_id):
    return controllers.update_wishlist_by_id(wishlist_id)

@wishlist.route('/wishlist/<wishlist_id>/delete', methods=['DELETE'])
def delete_wishlist_by_id(wishlist_id):
    return controllers.delete_wishlist_by_id(wishlist_id)