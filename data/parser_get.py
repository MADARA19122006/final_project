from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('check_in_from', type=str)
parser.add_argument('check_in_to', type=str)
