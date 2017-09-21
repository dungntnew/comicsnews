# -*- coding: utf-8 -*-

from comicnews.admin.views import Base
from wtforms import TextAreaField
from wtforms.widgets import TextArea


class PostView(Base):
    can_create = True
    can_delete = True
    can_edit = True

    column_list = ('id',
                   'text',
                   'published',
                   'created_date',
                   'modified_date'
                   )
    column_labels = {
        'id': '#',
        'text': u'内容',
        'published': u'公開',
        'created_date': u'作成時期',
        'modified_date': u'更新時期',
    }

    column_details_list = ('id', 'text', 'published', 'created_date', 'modified_date')
    form_columns = ('text', 'published')

    column_formatters = dict(text=lambda v, c, m, p: m.short_text())


class JSONTextAreaWidget(TextArea):
    def __call__(self, field, **kwargs):
        if kwargs.get('class'):
            kwargs['class'] += ' json-raw-text'
        else:
            kwargs.setdefault('class', 'json-raw-text')
        return super(JSONTextAreaWidget, self).__call__(field, **kwargs)


class JSONTextAreaField(TextAreaField):
    widget = JSONTextAreaWidget()


class RawObjectView(Base):

    can_create = True
    can_delete = True
    can_edit = True

    column_list = ('id',
                   'json',
                   'created_date',
                   'modified_date'
                   )
    column_labels = {
        'id': '#',
        'json': u'データー',
        'created_date': u'作成時期',
        'modified_date': u'更新時期',
    }

    column_formatters = dict(json=lambda v, c, m, p: m.preview())

    form_overrides = {
        'json': JSONTextAreaField
    }
