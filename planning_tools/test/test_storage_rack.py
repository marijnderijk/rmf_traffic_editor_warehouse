import yaml
import pytest
from pathlib import Path
from map.polygons import StorageRack 
from pathlib import Path

# Define the path to your YAML file
YAML_FILE_PATH = Path(__file__).resolve().parent / 'yaml' 

# Fixture to load YAML data from the file
@pytest.fixture
def storage_racks_data():
    building_yaml_path = YAML_FILE_PATH / 'warehouse_building.building.yaml'
    with open(building_yaml_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data['levels']['warehouse_floor']['storage_racks']

# Test function to create StorageRack instances from YAML
def test_create_storage_racks(storage_racks_data):

    for rack_data in storage_racks_data:
        storage_rack = StorageRack.from_yaml(rack_data)
        print("Storage Rack created:", storage_rack)
        assert isinstance(storage_rack, StorageRack)

        assert len(storage_rack.vertex_indices) > 0
        assert len(storage_rack.params) > 0
        assert isinstance(storage_rack.name, str)
        assert isinstance(storage_rack.num_bays, int)
        assert isinstance(storage_rack.num_rows, int)
        # Add more assertions as needed for specific properties

        assert storage_rack.name == rack_data['parameters']['name'][1]
        assert storage_rack.num_bays == rack_data['parameters']['num_bays'][1]
        assert storage_rack.num_rows == rack_data['parameters']['num_rows'][1]
        assert storage_rack.units_per_bay == rack_data['parameters']['units_per_bay'][1]
        
        # Check default_unit_heights
        expected_heights = [
            rack_data['parameters'][f'unit_height_{i}'][1]
            for i in range(storage_rack.units_per_bay)
        ]
        assert storage_rack.default_unit_heights == expected_heights

# Run the test
if __name__ == '__main__':
    pytest.main(['-v', __file__])
