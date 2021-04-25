from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('check_in', type=str)
parser.add_argument('check_out', type=str)
