#!/usr/bin/env python
# -*- coding: utf-8 -*-

from flask_admin import Admin
from flask_sqlalchemy import SQLAlchemy

from comicnews.admin.views.post import PostView, RawObjectView
from comicnews.data.models import Post, RawObject


def create_admin(app, db, url_prefix):
    admin = Admin(app,
                  name=u'管理ページ',
                  base_template='admin/admin.html',
                  template_mode='bootstrap3'
                  )

    admin.add_view(PostView(Post, db.session, name=u'ニュース'))
    admin.add_view(RawObjectView(RawObject, db.session, name=u'Objects'))

    return admin
