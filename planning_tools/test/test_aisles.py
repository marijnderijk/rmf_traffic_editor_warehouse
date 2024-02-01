import pytest
import yaml
from pathlib import Path
from map.polygons import Aisle  # Replace 'your_module' with the actual module name where the Aisle class is defined

GLOBAL_YAML_BASE_PATH = Path(__file__).resolve().parent / 'yaml'

@pytest.fixture
def sample_aisles_data():
    building_yaml_path = GLOBAL_YAML_BASE_PATH / 'warehouse_building.building.yaml'
    # Assuming the YAML file is in the same directory as the test file
    with open(building_yaml_path, 'r') as file:
        yaml_data = yaml.load(file, Loader=yaml.CLoader)
    return yaml_data['levels']['warehouse_floor']['aisles']

def test_create_aisles(sample_aisles_data):

    for aisle_data in sample_aisles_data:
        aisle_instance = Aisle.from_yaml(aisle_data)
        
        # Ensure the creation is successful
        assert isinstance(aisle_instance, Aisle)

        # Additional assertions based on your requirements
        assert len(aisle_instance.vertex_indices) > 0
        assert len(aisle_instance.params) > 0
        assert isinstance(aisle_instance.name, str)
        assert isinstance(aisle_instance.is_main_aisle, bool)
