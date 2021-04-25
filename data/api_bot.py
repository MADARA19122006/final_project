from datetime import datetime
from flask import jsonify, Flask
from flask_restful import Api, Resource
from data import db_session
from data.availability import Availability
from sqlalchemy import func
from data.parser_bot import parser
from data.rooms import Rooms

app = Flask(__name__)
api = Api(app)


class Bot(Resource):
    def get(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        av = {}
        for room in db_sess.query(Rooms).all():
            qty = db_sess.query(func.min(Availability.quantity_rooms)).filter(
                Availability.room == room.id,
                Availability.date >= datetime.strptime(args['check_in'], '%Y%m%d'),
                Availability.date < datetime.strptime(args['check_out'], '%Y%m%d')).scalar()
            if qty:
                av[room.name_room] = qty
        return jsonify(av)
