from flask_restful import reqparse

parser = reqparse.RequestParser()
parser.add_argument('availability', required=True, type=dict, action='append')
