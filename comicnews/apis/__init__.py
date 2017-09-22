from flask_restplus import Api
from flask import Blueprint

from .news import api as ns1

blueprint = Blueprint('api', __name__)
api = Api(
    app=blueprint,
    title='comics news APIs',
    version='1.0',
    description='Draft version 1.0',
    doc='/'
)

api.add_namespace(ns1, path='/posts')


# ...

def get_instance():
    return api
