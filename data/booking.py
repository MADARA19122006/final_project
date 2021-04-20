import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Booking(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'booking'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    room = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rooms.id"))
    guest = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("guests.id"))
    check_in = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    check_out = sqlalchemy.Column(sqlalchemy.Date, nullable=True)
    quantity = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    status = sqlalchemy.Column(sqlalchemy.Boolean, nullable=True)
    number_booking = sqlalchemy.Column(sqlalchemy.Integer, nullable=True)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    rooms = orm.relation('Rooms')
    guests = orm.relation('Guests')
