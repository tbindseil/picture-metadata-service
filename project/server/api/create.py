from project.server.log import INFO, WARN

from flask import request, make_response, jsonify
from flask.views import MethodView

from project.server import db
from project.server.models import Example
from project.server.models import Picture

from project.server.dwf.clients.auth.apis import AuthException, authenticate

class CreatePictureAPI(MethodView):
    """
    Create Picture and its metadata
    """
    def post(self):
        try:
            post_data = request.get_json()
            title = post_data.get('title')
            auth_header = request.headers.get('Authorization')
            if auth_header:
                token = auth_header.split(" ")[1]
            else:
                token = ''

            user = authenticate(token)

            picture = Picture.query.filter_by(title=title, creator=user.username).first()
            if not picture:
                picture = Picture(title=title, creator=user.username)
                # insert the example
                db.session.add(picture)
                db.session.commit()
                responseObject = {
                    'status': 'success',
                    'message': 'Successfully created picture.',
                    'title': picture.title,
                    'creator': picture.creator
                }
                return make_response(jsonify(responseObject)), 201
            else:
                responseObject = {
                    'status': 'fail',
                    'message': 'Picture with title: ' + title + ' already exists.',
                }
                return make_response(jsonify(responseObject)), 202
        except AuthException as e:
            responseObject = {
                'status': 'fail',
                'message': 'Invalid auth token.'
            }
            return make_response(jsonify(responseObject)), 401
        except Exception as e:
            WARN("add", "exception: " + str(e))
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
