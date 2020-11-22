from project.server.log import INFO, WARN

import json

from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server import db
from project.server.models import Example

class GetAllExampleAPI(MethodView):
    """
    Get All Examples Resource
    """

    def get(self):
        try:
            examples = Example.query.all()
            fields = []
            for example in examples:
                fields.append(example.field)
            responseObject = {
                'status': 'success',
                'message': 'Successfully get all examples.',
                'fields': json.dumps(fields)
            }
            return make_response(jsonify(responseObject)), 201
        except Exception as e:
            WARN("add", "exception: " + str(e))
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
