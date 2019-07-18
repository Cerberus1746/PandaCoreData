'''
:created: 17-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''
import pytest

from panda_core_data import data_core
from panda_core_data.custom_exceptions import (DuplicatedDataTypeName, DataTypeGroupNotFound,
                                               DataTypeNotFound, CannotInstanceTemplateDirectly)
from panda_core_data.template import Template

#pylint: disable=unused-import
from . import MODEL_TYPE_NAME

class TestTemplates(object):
    @staticmethod
    def test_check_if_created(template, second_template):
        assert template in data_core.all_templates
        assert second_template in data_core.all_templates

    @staticmethod
    def test_check_if_unequal(template, second_template):
        assert template != second_template

    @staticmethod
    def test_exceptions(template):
        #pylint: disable=unused-variable
        with pytest.raises(DataTypeGroupNotFound):  # @UndefinedVariable
            #pylint: disable=unused-variable
            class GroupTesting(Template, template_group_name="invalid", auto_create_group=False):
                name: str

        #pylint: disable=unused-variable
        with pytest.raises(DataTypeNotFound):  # @UndefinedVariable
            data_core.get_template_type("invalid")

        #pylint: disable=unused-variable
        with pytest.raises(DuplicatedDataTypeName):  # @UndefinedVariable
            class TestTemplate(Template, template_name=MODEL_TYPE_NAME):
                name: str

        #pylint: disable=unused-variable
        with pytest.raises(CannotInstanceTemplateDirectly):  # @UndefinedVariable
            template()
