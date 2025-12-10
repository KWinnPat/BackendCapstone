import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Items(db.Model):
    __tablename__ = "Items"

    item_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    category_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Categories.category_id'), nullable=False)
    name = db.Column(db.String(), nullable=False)
    details = db.Column(db.String(), nullable=True)
    price = db.Column(db.Float(), nullable=True)
    currency = db.Column(db.String(), nullable=True)
    shop_url = db.Column(db.String(), nullable=True)
    image_url = db.Column(db.String(), nullable=True)
    date_created = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    category = db.relationship('Categories', back_populates='items')
    wishlists = db.relationship('WishlistItems', back_populates='item')


    def __init__(self, category_id, name, details, price, currency, shop_url, image_url, date_created):
        self.category_id = category_id
        self.name = name
        self.details = details
        self.price = price
        self.currency = currency
        self.shop_url = shop_url
        self.image_url = image_url
        self.date_created = date_created

    def new_item_obj():
        return Items('', '', '', 0, '', '', '', db.func.current_timestamp())
    
class ItemSchema(ma.Schema):
    class Meta:
        fields = ['item_id', 'category', 'name', 'details', 'price', 'currency', 'shop_url', 'image_url', 'date_created']

    item_id = ma.fields.UUID()
    category = ma.fields.Nested('CategorySchema')
    name = ma.fields.String(required=True)
    details = ma.fields.String(allow_none=True)
    price = ma.fields.Float(allow_none=True)
    currency = ma.fields.String(allow_none=True)
    shop_url = ma.fields.String(allow_none=True)
    image_url = ma.fields.String(allow_none=True)
    date_created = ma.fields.DateTime(required=True, dump_default=db.func.current_timestamp())


item_schema = ItemSchema()
items_schema = ItemSchema(many=True)