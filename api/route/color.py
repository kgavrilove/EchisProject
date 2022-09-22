import datetime
import json
from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from

from api.service.AssetService import AssetService

color_api = Blueprint('color_api', __name__)
asset_service = AssetService()


@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Dominant colors method ',
        }
    }
})
@color_api.route('/dominant', methods=['POST','GET'])
def dominant():
    if request.method == 'POST':

        if not request.args.get('img') or not request.args.get('kClusters'):
            return json.dumps({
                'code': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                'error': 'invalid arguments',
                'date': datetime.datetime.now()
            }, indent=4, default=str), HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            img = request.args.get('img')  # D:\posters\1055_125.jpg
            k_clusters = int(request.args.get('kClusters'))
        except Exception as e:
            return json.dumps({
                'code': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                'error': e,
                'date': datetime.datetime.now()
            }, indent=4, default=str), HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            path = img
            data = asset_service.generate_info(path, k_clusters)

            output = {
                'code': HTTPStatus.OK,
                'date': datetime.datetime.now(),
                'path_debug': path,
                'k_clusters': k_clusters,
                'data': data

            }
            return json.dumps(output, indent=4, default=str), HTTPStatus.OK
        except Exception as e:
            return json.dumps({
                'code': HTTPStatus.BAD_REQUEST,
                'message': HTTPStatus.BAD_REQUEST.description,
                'error': e,
                'date': datetime.datetime.now(),
            }, indent=4, default=str), 400

    return json.dumps({
        'code':HTTPStatus.BAD_REQUEST,
        'message': HTTPStatus.BAD_REQUEST.description,
        'date': datetime.datetime.now(),
    }, indent=4, default=str), HTTPStatus.BAD_REQUEST

