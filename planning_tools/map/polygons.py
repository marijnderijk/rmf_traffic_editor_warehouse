from pydantic import BaseModel, Field
from .param_value import ParamValue 
from .vertex import Vertex

class Polygon(BaseModel):
    vertex_indices: list
    params: dict = Field(default_factory=dict)

    class Config:
        validate_assignment = True

    @classmethod
    def from_yaml(cls, yaml_node):
        return cls(
            vertex_indices=yaml_node.get('vertices', []),
            params={
                param_name: ParamValue.from_yaml(param_yaml)
                for param_name, param_yaml in yaml_node.get('parameters', {}).items()
            }
        )

    def to_yaml(self):
        return {
            'vertices': self.vertex_indices,
            'parameters': {
                param_name: param_value.to_yaml()
                for param_name, param_value in self.params.items()
            }
        }
    
    def __str__(self):
        return f'polygon ({len(self.vertex_indices)} vertices)'

    def __repr__(self):
        return self.__str__()

class Aisle(Polygon):
    name: str = Field(default='')
    is_main_aisle: bool = False

    @classmethod
    def from_yaml(cls, yaml_node):
        instance = super().from_yaml(yaml_node)
        # check if the name is in the parameters
        if 'name' in instance.params:
            instance.name = instance.params['name'].value

        if 'is_main_aisle' in instance.params:
            instance.is_main_aisle = instance.params['is_main_aisle'].value
        return instance

    def __str__(self):
        return f'aisle ({len(self.vertex_indices)} vertices, name={self.name}, is_main_aisle={self.is_main_aisle})'

    def __repr__(self):
        return self.__str__()

class Floor(Polygon):
    name: str = Field(default='')

    @classmethod
    def from_yaml(cls, yaml_node):
        instance = super().from_yaml(yaml_node)
        # check if the name is in the parameters
        if 'name' in instance.params:
            instance.name = instance.params['name'].value
        return instance

    def __str__(self):
        return f'floor ({len(self.vertex_indices)} vertices, name={self.name})'

    def __repr__(self):
        return self.__str__()


class StorageRack(Polygon):
    name: str = Field(default='')
    num_bays: int = 0
    num_rows: int = 0
    default_unit_heights: list[int] = Field(default_factory=list)
    units_per_bay: int = 0

    @classmethod
    def from_yaml(cls, yaml_node):
        instance = super().from_yaml(yaml_node)
        # check if the name is in the parameters
        if 'name' in instance.params:
            instance.name = instance.params['name'].value

        if 'num_bays' in instance.params:
            instance.num_bays = instance.params['num_bays'].value

        if 'num_rows' in instance.params:
            instance.num_rows = instance.params['num_rows'].value

        if 'units_per_bay' in instance.params:
            instance.units_per_bay = instance.params['units_per_bay'].value

        # check all the "unit_height_x" parameters
        instance.default_unit_heights = []
        for i in range(instance.units_per_bay):
            param_name = f'unit_height_{i}'
            if param_name in instance.params:
                instance.default_unit_heights.append(instance.params[param_name].value)

        return instance

    def __str__(self):
        return f'storage_rack ({len(self.vertex_indices)} vertices, name={self.name}, num_bays={self.num_bays}, num_rows={self.num_rows}, units_per_bay={self.units_per_bay})'

    def __repr__(self):
        return self.__str__()

class RackBay(Polygon):
    name: str = Field(default='')
    num_units: int = 0
    number: int = 0
    row: int = 0
    unit_heights: list[int] = Field(default_factory=list)
    parent_rack_name: str = Field(default='')
    parent_rack: StorageRack | None = None
    view_point: Vertex | None = None

    @classmethod
    def from_yaml(cls, yaml_node):
        instance = super().from_yaml(yaml_node)
        # check if the name is in the parameters
        if 'name' in instance.params:
            instance.name = instance.params['name'].value

        if 'n_units' in instance.params:
            instance.num_units = instance.params['n_units'].value

        if 'number' in instance.params:
            instance.number = instance.params['number'].value

        if 'row' in instance.params:
            instance.row = instance.params['row'].value

        if 'parent_rack_name' in instance.params:
            instance.parent_rack_name = instance.params['parent_rack_name'].value
    
        instance.unit_heights = []
        for i in range(instance.num_units):
            param_name = f'unit_height_{i}'
            if param_name in instance.params:
                instance.unit_heights.append(instance.params[param_name].value)

        return instance

    def set_parent_rack(self, parent_rack: StorageRack):
        self.parent_rack = parent_rack

    def set_view_point(self, view_point: Vertex):
        self.view_point = view_point

    def __str__(self):
        return f'rack_bay ({len(self.vertex_indices)} vertices, name={self.name}, number={self.number}, row={self.row}, parent_rack_name={self.parent_rack_name})'

    def __repr__(self):
        return self.__str__()





