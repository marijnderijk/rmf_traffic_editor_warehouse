import yaml
import pytest
from pathlib import Path
from map.polygons import Aisle, StorageRack, RackBay
from map.vertex import Vertex
from map.level import Level

GLOBAL_YAML_BASE_PATH = Path(__file__).resolve().parent / 'yaml'

@pytest.fixture
def sample_yaml_node():
    building_yaml_path = GLOBAL_YAML_BASE_PATH / 'warehouse_building.building.yaml'
    with open(building_yaml_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data['levels']

def test_level_creation(sample_yaml_node):
    first_level_name = list(sample_yaml_node.keys())[0]
    level_instance = Level.from_yaml(sample_yaml_node[first_level_name], first_level_name)

    assert level_instance.name == 'warehouse_floor'
    assert len(level_instance.aisles) > 0
    assert len(level_instance.storage_racks) > 0
    assert len(level_instance.vertices) > 0

    # check if the vertex indices of the polygons are valid
    for aisle in level_instance.aisles:
        for vertex_index in aisle.vertex_indices:
            assert vertex_index < len(level_instance.vertices)

    for storage_rack in level_instance.storage_racks:
        for vertex_index in storage_rack.vertex_indices:
            assert vertex_index < len(level_instance.vertices)

    for rack_bay in level_instance.rack_bays:
        for vertex_index in rack_bay.vertex_indices:
            assert vertex_index < len(level_instance.vertices)

    # check if the amount of rack bays is correct
    expected_rack_bays = 0
    for storage_rack in level_instance.storage_racks:
        expected_rack_bays += storage_rack.num_bays * storage_rack.num_rows

    assert len(level_instance.rack_bays) == expected_rack_bays
