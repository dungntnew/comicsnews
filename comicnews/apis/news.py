from flask import current_app
from flask_restplus import Namespace, Resource, fields

from comicnews.data import query_helper

api = Namespace('posts', description='Posts related operations')

post = api.model('Post', {
    'id': fields.String(required=True, readOnly=True, description='The post identifier'),
    'title': fields.String(required=True, description='The post title'),
    'url': fields.String(required=True, description='The post url'),
    'published': fields.String(required=True, description='The post published date'),
    'text': fields.String(required=True, description='The post tags'),
    'images': fields.List(fields.String, required=True, description='The post image urls'),
    'tags': fields.List(fields.String, required=True, description='The post tags'),
})


class PostDAO(object):
    def __init__(self):
        super()

    def list(self):
        return query_helper.latest_raw_objects()

    def get(self, id):
        item = query_helper.post_by_id(id)
        if item:
            return item
        api.abort(404, "Post {} doesn't exist".format(id))

    def create(self, data):
        return query_helper.create_post(data)

    def update(self, id, data):
        item = query_helper.update_post(id, data)
        if item:
            return item
        api.abort(404, "Post {} doesn't exist".format(id))

    def delete(self, id):
        query_helper.delete_post_by_id(id)


DAO = PostDAO()


def get_instance():
    return api.apis[0]


@api.route('/')
class PostList(Resource):
    """Shows a list of all posts, and lets you POST to add new posts"""

    @api.doc('list_post')
    @api.marshal_list_with(post)
    def get(self):
        """List all posts"""
        posts = DAO.list()
        return posts

    @api.doc('create_todo')
    @api.expect(post)
    @api.marshal_with(post, code=201)
    def post(self):
        """Create a new post"""
        current_app.logger.info('data: ', get_instance().payload)
        return DAO.create(get_instance().payload), 201


@api.route('/<id>')
@api.param('id', 'The post identifier')
@api.response(404, 'Post not found')
class Post(Resource):
    """Show a single todo item and lets you delete them"""

    @api.doc('get_post')
    @api.marshal_with(post)
    def get(self, id):
        """Fetch a post given its identifier"""
        return DAO.get(id)

    @api.doc('delete_post')
    @api.response(204, 'Post deleted')
    def delete(self, id):
        '''Delete a post given its identifier'''
        DAO.delete(id)
        return '', 204

    @api.doc('update_post')
    @api.expect(post)
    @api.marshal_with(post)
    def put(self, id):
        """Update a post given its identifier"""
        return DAO.update(id, get_instance().payload)
