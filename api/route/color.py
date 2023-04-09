import datetime
import json
from http import HTTPStatus
from flask import Blueprint, request
from flasgger import swag_from

from api.service.AssetService import AssetService
from api.service.BackgroundService import BackgroundService

color_api = Blueprint('color_api', __name__)
asset_service = AssetService()
background_service = BackgroundService()


@swag_from({
    'responses': {
        HTTPStatus.OK.value: {
            'description': 'Dominant colors method ',
        }
    }
})
@color_api.route('/dominant', methods=['POST', 'GET'])
def dominant():
    if request.method == 'POST':

        print(request.args)
        if not request.args.get('img') or not request.args.get('kClusters'):
            return json.dumps({
                'code': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                'error': 'invalid arguments',
                'method': '/dominant',
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
                'method': '/dominant',
                'date': datetime.datetime.now()
            }, indent=4, default=str), HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            path = img
            data = asset_service.generate_info(path, k_clusters)

            output = {
                'code': HTTPStatus.OK,
                'date': datetime.datetime.now(),
                'path_debug': path,
                'method': '/dominant',
                'k_clusters': k_clusters,
                'data': data

            }
            return json.dumps(output, indent=4, default=str), HTTPStatus.OK
        except Exception as e:
            return json.dumps({
                'code': HTTPStatus.BAD_REQUEST,
                'message': HTTPStatus.BAD_REQUEST.description,
                'error': e,
                'method': '/dominant',
                'date': datetime.datetime.now(),
            }, indent=4, default=str), 400

    return json.dumps({
        'code': HTTPStatus.BAD_REQUEST,
        'message': HTTPStatus.BAD_REQUEST.description,
        'method': '/dominant',
        'date': datetime.datetime.now(),
    }, indent=4, default=str), HTTPStatus.BAD_REQUEST


@color_api.route('/removeBackground', methods=['POST', 'GET'])
def remove_background():
    if request.method == 'POST':

        print(request.args)
        if not request.args.get('img'):
            return json.dumps({
                'code': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                'error': 'invalid arguments',
                'method': '/removeBackground',
                'date': datetime.datetime.now()
            }, indent=4, default=str), HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            img = request.args.get('img')  # D:\posters\1055_125.jpg

        except Exception as e:
            return json.dumps({
                'code': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                'error': e,
                'method': '/removeBackground',
                'date': datetime.datetime.now()
            }, indent=4, default=str), HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            img_path = img
            data = background_service.splitimage_tobytes(img_path)

            output = {
                'code': HTTPStatus.OK,
                'method': '/removeBackground',
                'date': datetime.datetime.now(),
                'path_debug': img_path,
                'data': data

            }
            return json.dumps(output, indent=4, default=str), HTTPStatus.OK
        except Exception as e:
            return json.dumps({
                'code': HTTPStatus.BAD_REQUEST,
                'message': HTTPStatus.BAD_REQUEST.description,
                'error': e,
                'method': '/removeBackground',
                'date': datetime.datetime.now(),
            }, indent=4, default=str), 400

    return json.dumps({
        'code': HTTPStatus.BAD_REQUEST,
        'message': HTTPStatus.BAD_REQUEST.description,
        'method': '/removeBackground',
        'date': datetime.datetime.now(),
    }, indent=4, default=str), HTTPStatus.BAD_REQUEST


@color_api.route('/itenAnalisys', methods=['POST', 'GET'])
def itenAnalisys():
    if request.method == 'POST':

        print(request.args)
        if not request.args.get('img'):
            return json.dumps({
                'code': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                'error': 'invalid arguments',
                'method': '/itenAnalisys',
                'date': datetime.datetime.now()
            }, indent=4, default=str), HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            img = request.args.get('img')  # D:\posters\1055_125.jpg
            mode = 'rgb'

        except Exception as e:
            return json.dumps({
                'code': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                'error': e,
                'method': '/itenAnalisys',
                'date': datetime.datetime.now()
            }, indent=4, default=str), HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            img_path = img
            #data = asset_service.iten_map(img_path, mode=mode)
            data = asset_service.iten_colors(img_path)

            output = {
                'code': HTTPStatus.OK,
                'date': datetime.datetime.now(),
                'method': '/itenAnalisys',
                'path_debug': img_path,
                'data': data

            }
            return json.dumps(output, indent=4, default=str), HTTPStatus.OK
        except Exception as e:
            return json.dumps({
                'code': HTTPStatus.BAD_REQUEST,
                'message': HTTPStatus.BAD_REQUEST.description,
                'error': e,
                'method': '/itenAnalisys',
                'date': datetime.datetime.now(),
            }, indent=4, default=str), 400

    return json.dumps({
        'code': HTTPStatus.BAD_REQUEST,
        'message': HTTPStatus.BAD_REQUEST.description,
        'method': '/itenAnalisys',
        'date': datetime.datetime.now(),
    }, indent=4, default=str), HTTPStatus.BAD_REQUEST

@color_api.route('/extractCounts', methods=['POST', 'GET'])
def extractCounts():
    if request.method == 'POST':

        print(request.args)
        if not request.args.get('img'):
            return json.dumps({
                'code': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                'error': 'invalid arguments',
                'method': '/extractCounts',
                'date': datetime.datetime.now()
            }, indent=4, default=str), HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            img = request.args.get('img')  # D:\posters\1055_125.jpg

        except Exception as e:
            return json.dumps({
                'code': HTTPStatus.UNPROCESSABLE_ENTITY,
                'message': HTTPStatus.UNPROCESSABLE_ENTITY.phrase,
                'error': e,
                'method': '/extractCounts',
                'date': datetime.datetime.now()
            }, indent=4, default=str), HTTPStatus.UNPROCESSABLE_ENTITY

        try:
            img_path = img
            data = asset_service.counts(img)

            output = {
                'code': HTTPStatus.OK,
                'date': datetime.datetime.now(),
                'method': '/extractCounts',
                'path_debug': img_path,
                'data': data

            }
            return json.dumps(output, indent=4, default=str), HTTPStatus.OK
        except Exception as e:
            return json.dumps({
                'code': HTTPStatus.BAD_REQUEST,
                'message': HTTPStatus.BAD_REQUEST.description,
                'error': e,
                'method': '/extractCounts',
                'date': datetime.datetime.now(),
            }, indent=4, default=str), 400

    return json.dumps({
        'code': HTTPStatus.BAD_REQUEST,
        'message': HTTPStatus.BAD_REQUEST.description,
        'method': '/extractCounts',
        'date': datetime.datetime.now(),
    }, indent=4, default=str), HTTPStatus.BAD_REQUEST