import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from .user_reservation_xref import user_reservation_association_table

class Reservations(db.Model):
    __tablename__ = "Reservations"

    reservation_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    xref_id = db.Column(UUID(as_uuid=True), db.ForeignKey('WishlistItems.xref_id'), nullable=False)
    quantity_reserved = db.Column(db.Integer(), nullable=True, default=1)
    gift_message = db.Column(db.String(), nullable=True)
    status = db.Column(db.String(), nullable=False, default='reserved')
    date_reserved = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())
    date_purchased = db.Column(db.DateTime(), nullable=True)
    date_updated = db.Column(db.DateTime(), nullable=True)

    wishlist_item = db.relationship('WishlistItems', back_populates='reservations')
    user = db.relationship('Users', secondary=user_reservation_association_table, back_populates='reservations')

    def __init__(self, xref_id, quantity_reserved, gift_message, status, date_reserved, date_purchased, date_updated):
        self.xref_id = xref_id
        self.quantity_reserved = quantity_reserved
        self.gift_message = gift_message
        self.status = status
        self.date_reserved = date_reserved
        self.date_purchased = date_purchased
        self.date_updated = date_updated

    def new_reservation_obj():
        return Reservations('',1,'','reserved',db.func.current_timestamp(), None, None)
    
class ReservationSchema(ma.Schema):
    class Meta:
        fields = ['reservation_id', 'item', 'quantity_reserved', 'gift_message', 'status', 'date_reserved', 'date_purchased', 'date_updated', 'user']

    reservation_id = ma.fields.UUID()
    item = ma.fields.Nested('WishlistItemSchema')
    quantity_reserved = ma.fields.Integer(allow_none=True, dump_default=1)
    gift_message = ma.fields.String(allow_none=True)
    status = ma.fields.String(required=True, dump_default='reserved')
    date_reserved = ma.fields.DateTime(required=True, dump_default=db.func.current_timestamp())
    date_purchased = ma.fields.DateTime(allow_none=True)
    date_updated = ma.fields.DateTime(allow_none=True)

    user = ma.fields.Nested('UserSchema', many=True, exclude=('reservations',))


reservation_schema = ReservationSchema()
reservations_schema = ReservationSchema(many=True)