from db import db

user_reservation_association_table = db.Table(
    "UserReservationAssociation",
    db.Model.metadata,
    db.Column('user_id', db.ForeignKey('Users.user_id'), primary_key=True),
    db.Column('reservation_id', db.ForeignKey('Reservations.reservation_id'), primary_key=True)
)