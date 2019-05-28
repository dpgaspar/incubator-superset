# Licensed to the Apache Software Foundation (ASF) under one
# or more contributor license agreements.  See the NOTICE file
# distributed with this work for additional information
# regarding copyright ownership.  The ASF licenses this file
# to you under the Apache License, Version 2.0 (the
# "License"); you may not use this file except in compliance
# with the License.  You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing,
# software distributed under the License is distributed on an
# "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY
# KIND, either express or implied.  See the License for the
# specific language governing permissions and limitations
# under the License.
# pylint: disable=C,R,W
from flask_appbuilder import ModelRestApi
from flask_appbuilder.models.sqla.interface import SQLAInterface
from flask_babel import gettext as __
from flask_babel import lazy_gettext as _
from wtforms.validators import StopValidation

from superset import appbuilder
from superset.models.annotations import Annotation, AnnotationLayer
from .base import DeleteMixin, SupersetModelView


class AnnotationLayerModelView(SupersetModelView, DeleteMixin):
    datamodel = SQLAInterface(AnnotationLayer)

    list_title = _('List Annotation Layer')
    show_title = _('Show Annotation Layer')
    add_title = _('Add Annotation Layer')
    edit_title = _('Edit Annotation Layer')

    list_columns = ['id', 'name']
    edit_columns = ['name', 'descr']
    add_columns = edit_columns

    label_columns = {
        'name': _('Name'),
        'descr': _('Description'),
    }


appbuilder.add_view(
    AnnotationLayerModelView,
    'Annotation Layers',
    label=__('Annotation Layers'),
    icon='fa-comment',
    category='Manage',
    category_label=__('Manage'),
    category_icon='')


class AnnotationLayerModelApi(ModelRestApi):  # noqa
    datamodel = SQLAInterface(AnnotationLayer)
    allow_browser_login = True
    resource_name = 'annotationlayer'

    list_title = AnnotationLayerModelView.list_title
    show_title = AnnotationLayerModelView.show_title
    add_title = AnnotationLayerModelView.add_title
    edit_title = AnnotationLayerModelView.edit_title

    list_columns = AnnotationLayerModelView.list_columns
    edit_columns = AnnotationLayerModelView.edit_columns
    add_columns = edit_columns
    label_columns = AnnotationLayerModelView.label_columns
    description_columns = AnnotationLayerModelView.description_columns


appbuilder.add_api(AnnotationLayerModelApi)


class StartEndDttmValidator(object):
    """
    Validates dttm fields.
    """
    def __call__(self, form, field):
        if not form['start_dttm'].data and not form['end_dttm'].data:
            raise StopValidation(
                _('annotation start time or end time is required.'),
            )
        elif (form['end_dttm'].data and
                form['start_dttm'].data and
                form['end_dttm'].data < form['start_dttm'].data):
            raise StopValidation(
                _('Annotation end time must be no earlier than start time.'),
            )


class AnnotationModelView(SupersetModelView, DeleteMixin):  # noqa
    datamodel = SQLAInterface(Annotation)
    allow_browser_login = True

    list_title = _('List Annotation')
    show_title = _('Show Annotation')
    add_title = _('Add Annotation')
    edit_title = _('Edit Annotation')

    list_columns = ['layer', 'short_descr', 'start_dttm', 'end_dttm']
    edit_columns = [
        'layer', 'short_descr', 'long_descr', 'start_dttm', 'end_dttm',
        'json_metadata']

    add_columns = edit_columns

    label_columns = {
        'layer': _('Layer'),
        'short_descr': _('Short Descr'),
        'start_dttm': _('Start Dttm'),
        'end_dttm': _('End Dttm'),
        'long_descr': _('Long Descr'),
        'json_metadata': _('JSON Metadata'),
    }

    description_columns = {
        'json_metadata': 'This JSON represents any additional metadata this \
         annotation needs to add more context.',
    }

    validators_columns = {
        'start_dttm': [
            StartEndDttmValidator(),
        ],
    }

    def pre_add(self, obj):
        if not obj.start_dttm:
            obj.start_dttm = obj.end_dttm
        elif not obj.end_dttm:
            obj.end_dttm = obj.start_dttm

    def pre_update(self, obj):
        self.pre_add(obj)


appbuilder.add_view(
    AnnotationModelView,
    'Annotations',
    label=__('Annotations'),
    icon='fa-comments',
    category='Manage',
    category_label=__('Manage'),
    category_icon='')


class AnnotationModelApi(ModelRestApi):  # noqa
    datamodel = SQLAInterface(Annotation)
    allow_browser_login = True
    resource_name = 'annotation'

    list_title = AnnotationModelView.list_title
    show_title = AnnotationModelView.show_title
    add_title = AnnotationModelView.add_title
    edit_title = AnnotationModelView.edit_title

    label_columns = AnnotationModelView.label_columns

    list_columns = ['layer.id', 'layer.name', 'short_descr', 'start_dttm', 'end_dttm']
    show_columns = list_columns
    edit_columns = AnnotationModelView.edit_columns
    add_columns = edit_columns
    description_columns = AnnotationModelView.description_columns

    def pre_add(self, obj):
        if not obj.start_dttm:
            obj.start_dttm = obj.end_dttm
        elif not obj.end_dttm:
            obj.end_dttm = obj.start_dttm

    def pre_update(self, obj):
        self.pre_add(obj)


appbuilder.add_api(AnnotationModelApi)
