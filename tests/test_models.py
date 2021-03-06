'''
:created: 09-07-2019

:author: Leandro (Cerberus1746) Benedet Garcia
'''

from dataclasses import fields, dataclass
import pytest

from panda_core_data import data_core, DataCore
from panda_core_data.custom_exceptions import (PCDDuplicatedTypeName,
                                               PCDInvalidPath, PCDTypeError,
                                               PCDNeedsToBeInherited)

from panda_core_data.model import Model, Template

from . import (DEFAULT_TEST_FIELD_CONTENT, DEFAULT_TEST_FIELD_NAME,
               INSTANCE_ERROR, MODEL_TYPE_NAME, MODEL_WITH_INIT_NAME,
               YAML_CONTENT)

class TestModels():
    @staticmethod
    def test_check_compatibility():
        class TemplateWithoutDataClass(Template):
            name: str

        class ModelWithoutDataClass(Model):
            name: str

        @dataclass
        class WithDataClass():
            name: str

        zipped = zip(fields(TemplateWithoutDataClass),
                     fields(ModelWithoutDataClass), fields(WithDataClass))
        for template_data, model_data, with_data in zipped:
            assert template_data.name == model_data.name == with_data.name
            assert template_data.type == model_data.type == with_data.type

    @staticmethod
    def test_repr():
        DataCore(name="test_repr")
        class TemplateRepr(Template, data_name="template_repr",
                           core_name="test_repr"):
            name: str

        class ModelRepr(Model, core_name="test_repr"):
            name: str

        print(repr(TemplateRepr("Test")))
        print(repr(ModelRepr("Test")))
        print(repr(TemplateRepr("Test").wrapper))
        print(repr(ModelRepr("Test").wrapper))

    @staticmethod
    def test_default():
        assert data_core.get_model_type("invalid", default=False) is False
        assert data_core.get_template_type("invalid", default=False) is False

    @staticmethod
    def test_check_if_created(model, second_model, template, second_template):
        assert model in data_core.all_models
        assert second_model in data_core.all_models

        assert template in data_core.all_templates
        assert second_template in data_core.all_templates

    @staticmethod
    def test_check_if_unequal(model, second_model, model_with_init, template,
                              second_template):
        assert template != second_template
        assert model != second_model != model_with_init

    @staticmethod
    def test_direct_instance_dataclass():
        current_core = DataCore(name="direct_instance")
        class TemplateDirectInstance(Template, core_name="direct_instance"):
            name: str

        class ModelDirectInstance(Model, core_name="direct_instance"):
            name: str

        instanced = ModelDirectInstance(DEFAULT_TEST_FIELD_CONTENT)

        assert isinstance(instanced, ModelDirectInstance), INSTANCE_ERROR
        assert instanced
        assert getattr(instanced,
                       DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT
        assert instanced in current_core.all_model_instances

        instanced = TemplateDirectInstance(DEFAULT_TEST_FIELD_CONTENT)

        assert isinstance(instanced, TemplateDirectInstance), INSTANCE_ERROR
        assert getattr(instanced,
                       DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT

    @staticmethod
    def test_dataclass_with_init(model_with_init):
        model_type = data_core.get_model_type(MODEL_WITH_INIT_NAME)
        instanced = model_type()

        assert isinstance(instanced, model_with_init), INSTANCE_ERROR
        assert getattr(instanced,
                       DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT
        assert instanced in data_core.all_model_instances

    @staticmethod
    def test_load_from_file(tmpdir, model):
        tmp_dir = tmpdir.mkdir("raws")
        yaml_file = tmp_dir.join("test.yaml")
        yaml_file_path = str(yaml_file.realpath())

        yaml_file.write(YAML_CONTENT)

        instanced = model(db_file=yaml_file_path)
        assert isinstance(instanced, model), INSTANCE_ERROR
        assert getattr(instanced,
                       DEFAULT_TEST_FIELD_NAME) == DEFAULT_TEST_FIELD_CONTENT
        assert instanced in data_core.all_model_instances


    def test_post_init_with_file(self, tmpdir):
        #pylint: disable=unused-variable
        class TestModelWithPostInit(Model):
            name: str

            def __post_init__(self):
                default_field = DEFAULT_TEST_FIELD_NAME
                assert getattr(self,
                               default_field) == DEFAULT_TEST_FIELD_CONTENT
                self.name = "another_content"

        #pylint: disable=unused-variable
        class TestTemplateWithPostInit(Template):
            name: str

            def __post_init__(self):
                default_field = DEFAULT_TEST_FIELD_NAME
                assert getattr(self,
                               default_field) == DEFAULT_TEST_FIELD_CONTENT
                self.name = "another_content"

        model_class = data_core.get_model_type("TestModelWithPostInit")
        template_class = data_core.get_template_type("TestTemplateWithPostInit")

        tmp_dir = tmpdir.mkdir("raws")
        yaml_file = tmp_dir.join("test.yaml")
        yaml_file_path = str(yaml_file.realpath())

        yaml_file.write(YAML_CONTENT)

        instanced = model_class(db_file=yaml_file_path)
        assert isinstance(instanced, model_class), INSTANCE_ERROR
        assert getattr(instanced, DEFAULT_TEST_FIELD_NAME) == "another_content"
        assert instanced in data_core.all_model_instances

        instanced = template_class(db_file=yaml_file_path)
        assert isinstance(instanced, template_class), INSTANCE_ERROR
        assert getattr(instanced, DEFAULT_TEST_FIELD_NAME) == "another_content"
        assert instanced in data_core.all_template_instances

    @staticmethod
    def test_type_getters(model, template):
        model_type = data_core.get_model_type(MODEL_TYPE_NAME)
        template_type = data_core.get_template_type(MODEL_TYPE_NAME)

        assert model == model_type
        assert template == template_type

        default_model = data_core.get_model_type("invalid", default=False)
        default_template = data_core.get_template_type("invalid", default=False)

        assert default_model is False
        assert default_template is False

    @staticmethod
    def test_exceptions(model):
        with pytest.raises(PCDDuplicatedTypeName):
            #pylint: disable=unused-variable
            class TemplateDuplicateTest(Template, data_name="same"):
                name: str

            #pylint: disable=unused-variable
            class TemplateDuplicateTest1(Template, data_name="same"):
                name: str

        with pytest.raises(PCDTypeError):
            data_core.get_template_type("invalid")

        #=======================================================================
        # Model tests are below
        #=======================================================================
        with pytest.raises(PCDTypeError):
            class NoInstanceModel(Model):
                name: str

            NoInstanceModel.load_db(NoInstanceModel, "")

        with pytest.raises(PCDNeedsToBeInherited):
            Template()

        with pytest.raises(PCDDuplicatedTypeName):
            #pylint: disable=unused-variable
            class ModelDuplicatedTest(Model, data_name="same"):
                name: str

            #pylint: disable=unused-variable
            class ModelDuplicatedTest1(Model, data_name="same"):
                name: str

        with pytest.raises(PCDTypeError):
            data_core.get_model_type("invalid")

        with pytest.raises(PCDInvalidPath):
            model(db_file="invalid")

        #pylint: disable=unused-variable
        with pytest.raises(PCDDuplicatedTypeName):
            class TestModel(Model, data_name=MODEL_TYPE_NAME):
                name: str
