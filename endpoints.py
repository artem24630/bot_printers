from flask_restful import Resource, reqparse


class NotifyError(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("version")
        params = parser.parse_args()
