# -*- coding: utf-8 -*-

import logging
import json

from flask import (
    jsonify,
    Blueprint,
    request,
)

from comicnews.data.models import (
    Post, RawObject
)

API_VERSION = '1.0.0'

API_PREFIX = ''  # TODO: set perfix

mod_api = Blueprint('api', __name__, url_prefix='/api')

logger = logging.getLogger(__name__)


def parse_request_json():
    logger.info('[REQUEST] {0}'.format(request.data))

    if request.headers['content-type'] == 'application/json':
        try:
            return 200, json.loads(request.data.decode('utf-8'))
        except ValueError:
            return 405, None
    else:
        return 400, None


def parse_form_json(data_key):
    if data_key not in request.form:
        return 400, None
    data = request.form[data_key]

    try:
        return 200, json.loads(data)
    except ValueError:
        return 405, None


@mod_api.route('/stat', methods=['GET', 'POST'])
def status():
    response = {
        'status': 200,
        'message': 'alive!',
    }
    return jsonify(response), 200


@mod_api.route('/objects', methods=['GET'])
def get_objects():
    objects = RawObject.query.all()

    return jsonify({
        'status': 200,
        'error': None,
        'objects': [o.to_json() for o in objects]
    })
