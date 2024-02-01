import pytest
from map.param_value import ParamValue  # Replace 'your_module' with the actual module name

def test_param_value_creation_bool():
    yaml_value = [4, True]  # Note: using True without quotation marks
    param_instance = ParamValue.from_yaml(yaml_value)
    assert param_instance.type == ParamValue.BOOL
    assert param_instance.value is True

def test_param_value_creation_int():
    yaml_value = [2, 42]  # Note: using 42 without quotation marks
    param_instance = ParamValue.from_yaml(yaml_value)
    assert param_instance.type == ParamValue.INT
    assert param_instance.value == 42

def test_param_value_creation_string():
    yaml_value = [1, 'hello']  # Note: using 'hello' with quotation marks
    param_instance = ParamValue.from_yaml(yaml_value)
    assert param_instance.type == ParamValue.STRING
    assert param_instance.value == 'hello'
