from datetime import datetime

from flask import jsonify, Flask
from flask_restful import Api, Resource
from data import db_session
from data.availability import Availability
from data.parser_av import parser

app = Flask(__name__)
api = Api(app)


class AvailabilityAdd(Resource):
    def post(self):
        args = parser.parse_args()
        db_sess = db_session.create_session()
        for i in args['availability']:
            for ent in db_sess.query(Availability).filter(  # удаляем дубли записей
                    Availability.date == datetime.strptime(i['date'], '%Y%m%d').date(),
                    Availability.room == i['room']):
                db_sess.delete(ent)
            entry = Availability(
                date=datetime.strptime(i['date'], '%Y%m%d').date(),
                room=i['room'],
                quantity_rooms=i['qty'],
                price=i['price'])
            db_sess.add(entry)
            db_sess.commit()
        return jsonify({'success': 'OK'})