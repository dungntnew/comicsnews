import jsonschema
from jsonschema.exceptions import ValidationError

post_schema = {
    'type': 'object',
    'properties': {
        'url': {'type': 'string'},
        'title': {'type': 'string'},
        'published': {'type': 'string'},
        'images': {
            'type': 'array',
            'items': {'type': 'string'}
        },
        'tags': {
            'type': 'array',
            'items': {'type': 'string'}
        },
        'text': {'type': 'string'},
    },
    'required': ['url', 'title', 'text', 'images', 'tags']
}


def validate_post(data):
    try:
        jsonschema.validate(data, post_schema)
        return True, None
    except ValidationError as e:
        return False, e
