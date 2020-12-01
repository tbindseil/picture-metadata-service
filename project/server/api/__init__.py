from project.server.log import INFO

from flask import Blueprint, request, make_response, jsonify, g

from .add import AddExampleAPI
from .all import GetAllExampleAPI
from .create import CreatePictureAPI

# create blueprints
add_blueprint = Blueprint('add', __name__)
all_blueprint = Blueprint('all', __name__)
create_blueprint = Blueprint('create', __name__)

# define the API resources
add_view = AddExampleAPI.as_view('add_api')
all_view = GetAllExampleAPI.as_view('all_api')
create_view = CreatePictureAPI.as_view('create_api')

# add Rules for API Endpoints
add_blueprint.add_url_rule(
    '/example/add',
    view_func=add_view,
    methods=['POST']
)
all_blueprint.add_url_rule(
    '/example/all',
    view_func=all_view,
    methods=['GET']
)
create_blueprint.add_url_rule(
    '/picture-metadata/create',
    view_func=create_view,
    methods=['POST']
)

# TODO put in dwf.clients.auth somewhere,
# then call that with all authenticated bloueprints,
# so it can iterate and set all their before_request
# authentication method
from project.server.dwf.clients.auth.apis import AuthException, authenticate
def check_bearer_token():
    try:
        auth_header = request.headers.get('Authorization')
        if auth_header:
            token = auth_header.split(" ")[1]
        else:
            token = ''
        g.user = authenticate(token)
        return None
    except AuthException as e:
        responseObject = {
            'status': 'fail',
            'message': 'Invalid auth token.'
        }
        return make_response(jsonify(responseObject)), 401

# add_blueprint.before_request(check_bearer_token)
# all_blueprint.before_request(check_bearer_token)
create_blueprint.before_request(check_bearer_token)
