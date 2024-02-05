from pydantic import BaseModel, Field
from shapely.geometry import Point
from .param_value import ParamValue



class Vertex(BaseModel):
    x: float
    y: float
    z: float = 0  # Use Pydantic's default value for z
    name: str
    params: dict = Field(default_factory=dict)

    class Config:
        validate_assignment = True

    @classmethod
    def from_yaml(cls, yaml_node): # , coordinate_system):
        """
        Create a Vertex from a YAML node.
        :param yaml_node: A YAML node representing a Vertex.
        :return: A Vertex object.
        NOTE: we don't use the coordinate system here because we want to keep the
        original values from the YAML file.
        """
        return cls(
            x=float(yaml_node[0]),
            y=float(yaml_node[1]), # * coordinate_system.y_flip_scalar(),
            z=float(yaml_node[2]),
            name=yaml_node[3],
            params={
                param_name: ParamValue.from_yaml(param_yaml)
                for param_name, param_yaml in yaml_node[4].items()
            } if len(yaml_node) > 4 and yaml_node[4] else {}
        )

    def to_yaml(self): #, coordinate_system):
        return [
            self.x,
            self.y, # * coordinate_system.y_flip_scalar(),
            self.z,
            self.name,
            {
                param_name: param_value.to_yaml()
                for param_name, param_value in self.params.items()
            }
        ]

    def to_shapely_point(self):
        return Point(self.x, self.y)

    def shapely(self):
        return self.to_shapely_point()

    def __hash__(self):
        return hash((self.x, self.y, self.z, self.name, self.shapely()))


