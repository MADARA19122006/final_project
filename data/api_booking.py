from datetime import datetime
from flask import jsonify, Flask
from flask_restful import Api, Resource
from data import db_session
from data.booking import Booking
from data.parser_get import parser

app = Flask(__name__)
api = Api(app)


class BookingGet(Resource):
    def get(self):
        db_sess = db_session.create_session()
        args = parser.parse_args()
        s = {'booking': []}
        m = db_sess.query(Booking).filter(
            Booking.check_in >= datetime.strptime(args['check_in_from'], '%Y%m%d').date(),
            Booking.check_in <= datetime.strptime(args['check_in_to'], '%Y%m%d').date())
        for i in m:
            s['booking'].append(
                {'room': i.room, 'guest': i.guests.name, 'check_in': i.check_in.strftime('%Y-%m-%d'), 'check_out': i.check_out.strftime('%Y-%m-%d'), 'quantity': i.quantity,
                 'status': i.status, 'number_booking': i.number_booking, 'price': i.price})
        return jsonify(s)
