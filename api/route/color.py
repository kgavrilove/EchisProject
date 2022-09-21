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
            'description': 'healthcheck method ',
        }
    }
})
@color_api.route('/dominant', methods=['POST'])
def dominant():
    if request.method == 'POST':
        # add checking and try catch blocks
        img = request.args.get('img')
        k_clusters = int(request.args.get('k_clusters'))
        if k_clusters > 1:
            path = img
            data = asset_service.generate_info(path, k_clusters)

            output = {
                'status': HTTPStatus.OK,
                'path_debug': path,
                'k_clusters': k_clusters,
                'data': data
            }
            return json.dumps(output, indent=4, default=str), 200

    return 'img', 200
