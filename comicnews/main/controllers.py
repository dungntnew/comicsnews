from flask import Blueprint, current_app, render_template

from comicnews.cache import cache
from comicnews.data.query_helper import latest_raw_objects

main = Blueprint('main', __name__, template_folder='templates')


@main.route('/posts/')
@cache.cached(0)
def list_posts():
    posts = latest_raw_objects()
    current_app.logger.info(posts)

    current_app.logger.info('Displaying all raw-posts.')

    return render_template("posts.htm", posts=posts)
