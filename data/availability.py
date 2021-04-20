import sqlalchemy
from sqlalchemy_serializer import SerializerMixin
from data.db_session import SqlAlchemyBase
from sqlalchemy import orm


class Availability(SqlAlchemyBase, SerializerMixin):
    __tablename__ = 'availability'
    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    room = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey("rooms.id"))
    date = sqlalchemy.Column(sqlalchemy.Date)
    quantity_rooms = sqlalchemy.Column(sqlalchemy.Integer, nullable=True, default=0)
    price = sqlalchemy.Column(sqlalchemy.Integer, default=0)
    rooms = orm.relation('Rooms')
