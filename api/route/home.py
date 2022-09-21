import datetime
import json
from http import HTTPStatus
from flask import Blueprint
from flasgger import swag_from


home_api = Blueprint('api', __name__)

@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'healthcheck method ',
        }
    }
})
@home_api.route('/')
def welcome():
    """
    1 liner about the route
    A more detailed description of the endpoint
    ---
    """
    output={
        'status':HTTPStatus.OK,
        'date':datetime.datetime.now()
    }
    return json.dumps(output, indent=4, default=str), 200