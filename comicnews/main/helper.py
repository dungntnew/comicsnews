from flask import current_app

"""
convert raw json object to valid form
add flag where post is valid

  <th>{{ _('url') }}</th>
  <th>{{ _('title') }}</th>
  <th>{{ _('published') }}</th>
  <th>{{ _('images') }}</th>
  <th>{{ _('tags') }}</th>
  <th>{{ _('text') }}</th>

"""

FIELDS = ('url', 'title', 'published', 'images', 'tags', 'text')


def raw_to_post(object):

    current_app.logger.info("parsing: {}".format(object.id))

    raw = object.to_json()

    current_app.logger.info("raw: {}".format(raw))

    for key in FIELDS:
        if key not in raw:
            return {
                'valid': False
            }

    raw.update({
        'valid': True,
        'id': object.id,
        'created': object.created_date
    })
    current_app.logger.info(raw)
    return raw
