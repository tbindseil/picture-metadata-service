from project.server.log import INFO, WARN

from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server import db
from project.server.models import Example

from project.server.dwf.clients.auth.apis import authenticate

class AddExampleAPI(MethodView):
    """
    Create Picture and its metadata
    """
    def post(self):
        try:
            # get the post data
            post_data = request.get_json()
            title = post_data.get('title')
            auth_header = request.headers.get('Authorization')
            if auth_header:
                token = auth_header.split(" ")[1]
            else:
                token = ''

            authenticate()

            # user = ... # need to extract user from token
            # ^nope get token from ehader
            # check if example already exists
            picture = Example.query.filter_by(field=field).first()
            if not example:
                example = Example(field=field)
                # insert the example
                db.session.add(example)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully registered.',
                    'field': example.field
                }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Example with field: ' + field + ' already exists.',
                }
                return make_response(jsonify(responseObject)), 202
        except Exception as e:
            WARN("add", "exception: " + str(e))
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
