import pytest
import yaml
from map.vertex import Vertex
from map.param_value import ParamValue
from pathlib import Path

GLOBAL_YAML_BASE_PATH = Path(__file__).resolve().parent / 'yaml'

@pytest.fixture
def sample_yaml_node():
    test_yaml_path = GLOBAL_YAML_BASE_PATH / 'test_vertex.yaml'
    with open(test_yaml_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data['vertices'][0]

def test_vertex_creation(sample_yaml_node):
    vertex_instance = Vertex.from_yaml(sample_yaml_node)

    assert vertex_instance.x == 1825.325
    assert vertex_instance.y == 445.57900000000001
    assert vertex_instance.z == 0
    assert vertex_instance.name == 'rack_viewpoint_0_0'
    
    assert 'is_inspection_point' in vertex_instance.params
    param_value = vertex_instance.params['is_inspection_point']
    assert param_value.type == ParamValue.BOOL
    assert param_value.value is True

def test_vertex_to_yaml(sample_yaml_node):
    vertex_instance = Vertex.from_yaml(sample_yaml_node)
    yaml_representation = vertex_instance.to_yaml()

    # Assuming that 'yaml_representation' is similar to the input 'sample_yaml_node'
    assert yaml_representation == sample_yaml_node

# Add more test cases as needed
