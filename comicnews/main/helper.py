from comicnews.data.schemas import validate_post

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


def raw_to_post(data):
    raw = data.to_json()

    valid, _ = validate_post(raw)

    if not valid:
        return {
            'valid': False
        }

    raw.update({
        'valid': True,
        'id': data.id,
        'created': data.created_date
    })
    return raw
