import marshmallow as ma
import uuid
from sqlalchemy.dialects.postgresql import UUID

from db import db

class Events(db.Model):
    __tablename__ = "Events"

    event_id = db.Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = db.Column(db.String(), nullable=False)
    event_type = db.Column(db.String(), nullable=True)
    location = db.Column(db.String(), nullable=True)
    start_date = db.Column(db.DateTime(), nullable=True)
    end_date = db.Column(db.DateTime(), nullable=True)
    notes = db.Column(db.String(), nullable=True)
    date_created = db.Column(db.DateTime())
    date_updated = db.Column(db.DateTime(), nullable=True)

    def __init__(self, name, event_type, location, start_date, end_date, notes, date_created, date_updated):
        self.name = name
        self.event_type = event_type
        self.location = location
        self.start_date = start_date
        self.end_date = end_date
        self.notes = notes
        self.date_created = date_created
        self.date_updated = date_updated

class EventSchema(ms.Schema):
    class Meta:
        fields = ['event_id', 'name', 'event_type', 'location', 'start_date', 'end_date', 'notes', 'date_created', 'date_updated']

    event_id = ma.fields.UUID()
    name = ma.fields.String(required=True)
    event_type = ma.fields.String(allow_none=True)
    location = ma.fields.String(allow_none=True)
    start_date = ma.fields.DateTime(allow_none=True)
    end_date = ma.fields.DateTime(allow_none=True)
    notes = ma.fields.String(allow_none=True)
    date_created = ma.fields.DateTime(required=True)
    date_updated = ma.fields.DateTime(allow_none=True)

event_schema = EventSchema()