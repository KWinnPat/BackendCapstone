import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db
from .user_reservation_xref import user_reservation_association_table

class Users(db.Model):
    __tablename__ = "Users"

    user_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    username = db.Column(db.String(), nullable=False)
    email = db.Column(db.String(), nullable=False)
    password = db.Column(db.String(), nullable=False)
    role = db.Column(db.String(), nullable=False)
    is_active = db.Column(db.Boolean(), nullable=False, default=True)
    date_joined = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    wishlists = db.relationship('Wishlists', back_populates='user')
    reservations = db.relationship('Reservations', secondary=user_reservation_association_table, back_populates='user')
    auth = db.relationship('AuthTokens', back_populates='user')

    def __init__(self, username, email, password, role, is_active=True, date_joined=None):
        self.username = username
        self.email = email
        self.password = password
        self.role = role
        self.is_active = is_active
        self.date_joined = date_joined if date_joined else db.func.current_timestamp()


    def new_user_obj():
        return Users('', '', '', '', True, None)
    
class UserSchema(ma.Schema):
    class Meta:
        fields = ['user_id', 'username', 'email', 'role', 'is_active', 'date_joined', 'wishlists', 'reservations']
    user_id = ma.fields.UUID()
    username = ma.fields.String(required=True)
    email = ma.fields.String(required=True)
    role = ma.fields.String(required=True)
    is_active = ma.fields.Boolean(required=True, dump_default=True)
    date_joined = ma.fields.DateTime(required=True, dump_default=db.func.current_timestamp())
    wishlists = ma.fields.Nested('WishlistSchema', many=True, exclude=('user',))
    reservations = ma.fields.Nested('ReservationSchema', many=True, exclude=('user',))

user_schema = UserSchema()
users_schema = UserSchema(many=True)