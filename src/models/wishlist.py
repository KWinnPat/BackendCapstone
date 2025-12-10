import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Wishlists(db.Model):
    __tablename__ = "Wishlists"

    wishlist_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    user_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Users.user_id'), nullable=False)
    title = db.Column(db.String(), nullable=False)
    description = db.Column(db.String(), nullable=True)
    event_id = db.Column(UUID(as_uuid=True), db.ForeignKey('Events.event_id'), nullable=False)
    date_created = db.Column(db.DateTime, nullable=False, default=db.func.current_timestamp())
    date_edited = db.Column(db.DateTime, nullable=True)
    is_public = db.Column(db.Boolean(), default=False)

    user = db.relationship('Users', back_populates='wishlists')
    event = db.relationship('Events', back_populates='wishlists')
    items = db.relationship('WishlistItems', back_populates='wishlist')

    def __init__(self, user_id, title, description, event_id, date_created, date_edited, is_public):
        self.user_id = user_id
        self.title = title
        self.description = description
        self.event_id = event_id
        self.date_created = date_created
        self.date_edited = date_edited
        self.is_public = is_public

    def new_wishlist_obj():
        return Wishlists('','', '', '', None, None, False)
    
class WishlistSchema(ma.Schema):
    class Meta:
        fields = ['wishlist_id', 'user', 'title', 'description', 'event', 'date_created', 'date_edited', 'is_public', 'items']

    wishlist_id = ma.fields.UUID()
    user = ma.fields.Nested('UserSchema', exclude=('wishlists',))
    title = ma.fields.String(required=True)
    description = ma.fields.String(allow_none=True)
    event = ma.fields.Nested('EventSchema')
    date_created = ma.fields.DateTime(required=True, dump_default=db.func.current_timestamp())
    date_edited = ma.fields.DateTime(allow_none=True)
    is_public = ma.fields.Boolean(required=True, dump_default=False)
    items = ma.fields.Nested('WishlistItemSchema', many=True, exclude=('wishlist',))


wishlist_schema = WishlistSchema()
wishlists_schema = WishlistSchema(many=True)