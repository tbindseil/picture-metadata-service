from project.server.log import INFO, WARN

from flask import request, make_response, jsonify, g
from flask.views import MethodView

from project.server import db
from project.server.models import Example
from project.server.models import Picture


class CreatePictureAPI(MethodView):
    """
    Create Picture and its metadata
    """
    def post(self):
        try:
            post_data = request.get_json()
            title = post_data.get('title')
            user = g.user

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
        except Exception as e:
            WARN("add", "exception: " + str(e))
            responseObject = {
                'status': 'fail',
                'message': 'Some error occurred. Please try again.'
            }
            return make_response(jsonify(responseObject)), 401
