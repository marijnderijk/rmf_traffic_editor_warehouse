import yaml
import pytest
from pathlib import Path
from map.polygons import RackBay  # Replace 'your_module' with the actual module name

# Define the path to your YAML file
YAML_FILE_PATH = Path(__file__).resolve().parent / 'yaml' 

# Fixture to load YAML data from the file
@pytest.fixture
def rack_bays_data():
    building_yaml_path = YAML_FILE_PATH / 'warehouse_building.building.yaml'
    with open(building_yaml_path, 'r') as file:
        yaml_data = yaml.safe_load(file)
    return yaml_data['levels']['warehouse_floor']['rack_bays']

# Test function to create RackBay instances from YAML
def test_create_rack_bays(rack_bays_data):

    for bay_data in rack_bays_data:
        rack_bay = RackBay.from_yaml(bay_data)
        print("Rack Bay created:", rack_bay)

        # Assertions
        assert isinstance(rack_bay, RackBay)
        assert rack_bay.name == bay_data['parameters']['name'][1]
        assert rack_bay.num_units == bay_data['parameters']['n_units'][1]
        assert rack_bay.number == bay_data['parameters']['number'][1]
        assert rack_bay.row == bay_data['parameters']['row'][1]
        assert rack_bay.parent_rack_name == bay_data['parameters']['parent_rack_name'][1]

        # Check unit_heights
        expected_heights = [
            bay_data['parameters'][f'unit_height_{i}'][1]
            for i in range(rack_bay.num_units)
        ]
        assert rack_bay.unit_heights == expected_heights

# Run the test
if __name__ == '__main__':
    pytest.main(['-v', __file__])
