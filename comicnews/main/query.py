from comicnews.data.models import RawObject
from comicnews.main.helper import raw_to_post


def latest_raw_objects():
    posts = [raw_to_post(raw) for raw in RawObject.query.order_by(RawObject.created_date.desc()).limit(25).all()]
    posts = [post for post in posts if post and post['valid']]

    return posts
