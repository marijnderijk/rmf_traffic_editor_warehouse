from pydantic import BaseModel, Field
from .polygons import Aisle, StorageRack, RackBay
from .vertex import Vertex
from .param_value import ParamValue

class Level(BaseModel):
    name: str
    aisles: list[Aisle]
    storage_racks: list[StorageRack]
    rack_bays: list[RackBay]
    vertices: list[Vertex]
    params: dict = Field(default_factory=dict)

    class Config:
        validate_assignment = True

    @classmethod
    def from_yaml(cls, yaml_node, name: str):
        return cls(
            # get the keys from the yaml node
            name=name,
            aisles=[Aisle.from_yaml(aisle_yaml) for aisle_yaml in yaml_node.get('aisles', [])],
            storage_racks=[StorageRack.from_yaml(rack_yaml) for rack_yaml in yaml_node.get('storage_racks', [])],
            rack_bays=[RackBay.from_yaml(rack_bay_yaml) for rack_bay_yaml in yaml_node.get('rack_bays', [])],
            vertices=[Vertex.from_yaml(vertex_yaml) for vertex_yaml in yaml_node.get('vertices', [])],
            params={
                param_name: ParamValue.from_yaml(param_yaml)
                for param_name, param_yaml in yaml_node.get('parameters', {}).items()
            }
        )

    def to_yaml(self):
        return {
            'name': self.name,
            'aisles': [aisle.to_yaml() for aisle in self.aisles],
            'storage_racks': [rack.to_yaml() for rack in self.storage_racks],
            'rack_bays': [rack_bay.to_yaml() for rack_bay in self.rack_bays],
            'vertices': [vertex.to_yaml() for vertex in self.vertices],
            'parameters': {
                param_name: param_value.to_yaml()
                for param_name, param_value in self.params.items()
            }
        }

    def set_polygon_vertices(self):
        for polygon in self.aisles + self.storage_racks + self.rack_bays:
            polygon.set_vertices([self.vertices[i] for i in polygon.vertex_indices])

    def __str__(self):
        return f'level ({len(self.aisles)} aisles, {len(self.storage_racks)} storage racks, {len(self.rack_bays)} rack bays, {len(self.vertices)} vertices)'

    def __repr__(self):
        return self.__str__()
