import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class WishlistItems(db.Model):
    __tablename__ = "WishlistItems"

    xref_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    wishlist_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Wishlists.wishlist_id'), nullable=False)
    item_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Items.item_id'), nullable=False)
    priority = db.Column(db.Integer(), nullable=False, default = 1)
    quantity = db.Column(db.Integer(), nullable=False, default = 1)

    wishlist = db.relationship('Wishlists', back_populates='items')
    item = db.relationship('Items', back_populates='wishlists')
    reservations = db.relationship('Reservations', back_populates='wishlist_item')

    def __init__(self, wishlist_id, item_id, priority, quantity):
        self.wishlist_id = wishlist_id
        self.item_id = item_id
        self.priority = priority
        self.quantity = quantity

    def new_wishlist_item_obj():
        return WishlistItems('','',1,1)
    
class WishlistItemSchema(ma.Schema):
    class Meta:
        fields = ['xref_id', 'wishlist', 'item', 'priority', 'quantity']

    xref_id = ma.fields.UUID()
    wishlist = ma.fields.Nested('WishlistSchema')
    item = ma.fields.Nested('ItemSchema')
    priority = ma.fields.Integer(required=True, dump_default=1)
    quantity = ma.fields.Integer(required=True, dump_default=1)

wishlist_item_schema = WishlistItemSchema()
wishlist_items_schema = WishlistItemSchema(many=True)