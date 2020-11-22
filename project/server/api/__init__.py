from flask import Blueprint

from .add import AddExampleAPI
from .all import GetAllExampleAPI

# create blueprints
add_blueprint = Blueprint('add', __name__)
all_blueprint = Blueprint('all', __name__)

# define the API resources
add_view = AddExampleAPI.as_view('add_api')
all_view = GetAllExampleAPI.as_view('all_api')

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
