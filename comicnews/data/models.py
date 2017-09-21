import json
from flask_sqlalchemy import SQLAlchemy
from flask_security import UserMixin, RoleMixin
from flask import Markup

db = SQLAlchemy()


# base mode class
class Base(db.Model):
    __abstract__ = True

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())


class Post(Base):
    url = db.Column(db.UnicodeText)
    text = db.Column(db.UnicodeText)
    published = db.Column(db.String(255), default=None)
    images = db.Column(db.UnicodeText, default=None)
    tags = db.Column(db.UnicodeText, default=None)
    text = db.Column(db.UnicodeText, default=None)

    def short_text(self):
        if not self.text:
            return '<Empty>'
        return '%s...' % self.text[:80]

    def __unicode__(self):
        return self.short_text()


class RawObject(db.Model):
    id = db.Column(db.Integer(), primary_key=True)
    json = db.Column(db.UnicodeText)
    created_date = db.Column(db.DateTime, default=db.func.current_timestamp())
    modified_date = db.Column(db.DateTime, default=db.func.current_timestamp(),
                              onupdate=db.func.current_timestamp())

    def __repr__(self):
        return self.json

    def to_json(self):
        print("RAW: ", self.json)
        data = {}
        try:
            data = json.loads(self.json, strict=False)
        except Exception as e:
            print("LOAD: ", data, "Error: ", e)

        return data

    def short_text(self):
        return self.json[:80]

    def preview(self):
        try:
            data = json.loads(self.json, strict=False)
            data = json.dumps(data, sort_keys=True, indent=4, separators=(',', ':'))
            return Markup('<pre class="pre-json">%s</pre>') % (data)
        except Exception as e:
            return Markup('<pre class="pre-json">{}</pre>')


roles_users = db.Table('roles_users', \
                       db.Column('user_id', db.Integer(), db.ForeignKey('user.id')), \
                       db.Column('role_id', db.Integer(), db.ForeignKey('role.id')))


class Role(db.Model, RoleMixin):
    id = db.Column(db.Integer(), primary_key=True)
    name = db.Column(db.String(80), unique=True)
    description = db.Column(db.String(255))

    def __init__(self, name):
        self.name = name

    def __repr__(self):
        return '<Role %r>' % (self.name)


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True)
    password = db.Column(db.String(255))
    active = db.Column(db.Boolean())
    roles = db.relationship('Role', secondary=roles_users,
                            backref=db.backref('users', lazy='dynamic'))

    def __init__(self, email, password, active, roles):
        self.email = email
        self.password = password
        self.active = active
        self.roles = roles

    def __repr__(self):
        return '<User %r>' % (self.email)
