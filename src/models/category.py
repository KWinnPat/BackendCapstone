import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db


class Categories(db.Model):
    __tablename__ = "Categories"

    category_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False, unique=True)
    description = db.Column(db.String(), nullable=True)
    icon = db.Column(db.String(), nullable=True)
    color = db.Column(db.String(), nullable=False, default='#FFFFFF')
    date_created = db.Column(db.DateTime(), nullable=False, default=db.func.current_timestamp())

    items = db.relationship('Items', back_populates='category')

    def __init__(self, name, description, icon, color, date_created):
        self.name = name
        self.description = description
        self.icon = icon
        self.color = color
        self.date_created = date_created

    def new_category_obj():
        return Categories('', '', '', '#FFFFFF', db.func.current_timestamp())
    
class CategorySchema(ma.Schema):
    class Meta:
        fields = ['category_id', 'name', 'description', 'icon', 'color', 'date_created']
    
    category_id = ma.fields.UUID()
    name = ma.fields.String(required=True)
    description = ma.fields.String(allow_none=True)
    icon = ma.fields.String(allow_none=True)
    color = ma.fields.String(allow_none=True)
    date_created = ma.fields.DateTime(allow_none=False, dump_default=db.func.current_timestamp())

category_schema = CategorySchema()
categories_schema = CategorySchema(many=True)