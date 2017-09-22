import json
from comicnews.data.helper import raw_to_post, post_to_raw
from comicnews.data.models import db, RawObject


def latest_raw_objects():
    posts = [raw_to_post(raw) for raw in RawObject.query.order_by(RawObject.created_date.desc()).limit(25).all()]
    posts = [post for post in posts if post and post['valid']]

    return posts


def _post_to_json(post):
    try:
        post = raw_to_post(post)
        if post['valid']:
            return post
    except Exception as _:
        pass
    return None


def post_by_id(id):
    post = RawObject.query.get(id)
    return _post_to_json(post)


def update_post(id, data):
    post = RawObject.query.get(id)
    try:
        # save post data as raw json
        raw = raw_to_post(post)
        raw.update(data)
        raw = post_to_raw(raw)
        raw = json.dumps(raw, indent=4, sort_keys=True, default=str)
        post.json = raw
        db.session.commit()

        # re-create json for response
        post = raw_to_post(post)
        if post['valid']:
            return post
    except Exception as _:
        pass
    return None


def create_post(data):
    try:
        post = RawObject(json=json.dumps(data))
        db.session.add(post)
        db.session.commit()

        # re-create json for response
        post = raw_to_post(post)
        if post['valid']:
            return post

    except Exception as _:
        return None


def delete_post_by_id(id):
    try:
        RawObject.query.filter_by(id=id).delete()
        db.session.commit()
    except Exception as _:
        pass
