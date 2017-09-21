# -*- coding: utf-8 -*-

from flask_admin.contrib.sqla import ModelView
from flask_admin.model import typefmt
from datetime import date


def date_format(view, value):
    return value.strftime('%Y-%m-%d')


MY_DEFAULT_FORMATTERS = dict(typefmt.BASE_FORMATTERS)
MY_DEFAULT_FORMATTERS.update({
    type(None): typefmt.null_formatter,
    date: date_format
})


# -- region ModelViews ------------
class Base(ModelView):
    page_size = 50
    can_view_details = True

    can_create = False
    can_delete = False
    can_edit = False
    can_export = False

    # create_modal = True
    # edit_modal = True
    # details_modal = True
    # export_max_rows = 0;

    column_display_pk = True
    form_excluded_columns = ('created_date', 'modified_date')
    column_type_formatters = MY_DEFAULT_FORMATTERS
