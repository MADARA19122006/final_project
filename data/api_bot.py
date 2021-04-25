from datetime import datetime
from flask import jsonify, Flask
from flask_restful import Api, Resource
from data import db_session
from data.availability import Availability
from sqlalchemy import func
from data.parser_bot import parser

app = Flask(__name__)
api = Api(app)


class Bot(Resource):
    def get(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        x = db_sess.query(func.min(Availability.quantity_rooms)).filter(
            Availability.date >= datetime.strptime(args['check_in'], '%Y%m%d'),
            Availability.date < datetime.strptime(args['check_out'], '%Y%m%d')).scalar()
        return jsonify({'quantity_rooms': x})
