from comicnews import app
from comicnews.data.models import db, RawObject
from flask_security.utils import encrypt_password

from faker import Faker
from random import randint
import json


def create_raw_objects():
    fake = Faker()
    img = "http://via.placeholder.com/200x150"
    for _ in range(100):
        db.session.add(RawObject(json=json.dumps({
            'url': 'http://google.com',
            'title': fake.text()[:10],
            'images': [img for _ in range(randint(1, 5))],
            'tags': [fake.text()[:3] for _ in range(randint(3, 6))],
            'published': "2017年{}月{}日".format(randint(1, 12), randint(1, 30)),
            'text': fake.text()
        })))
    db.session.commit()


def create_roles(data_store):
    data_store.create_role(name='admin')
    data_store.commit()


def create_users(data_store):
    users = [('admin@test.com', 'admin', '1234', ['admin'], True), \
             ('user@test.com', 'user', '6789', [], True)]
    for user in users:
        email = user[0]
        username = user[1]
        password = user[2]
        is_active = user[4]
        if password is not None:
            password = encrypt_password(password)
        roles = [data_store.find_or_create_role(rn) for rn in user[3]]
        data_store.commit()
        user = data_store.create_user(email=email, password=password, active=is_active)
        data_store.commit()
        for role in roles:
            data_store.add_role_to_user(user, role)
        data_store.commit()


data_store = app.security.datastore
with app.app_context():
    db.drop_all()
    db.create_all()

    create_roles(data_store)
    create_users(data_store)
    create_raw_objects()
