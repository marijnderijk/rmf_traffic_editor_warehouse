from pydantic import BaseModel, Field
import networkx as nx
from shapely.geometry import Point, Polygon as ShapelyPolygon
from shapely.strtree import STRtree
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

    def create_network(self):
        # create a networkx graph
        G = nx.DiGraph()

        # Define weight constants for moving to main
        # and secondary aisles
        MAIN_AISLE_WEIGHT = 1
        NON_MAIN_AISLE_WEIGHT = 10

        # Add the aisles to the graph
        for aisle in self.aisles:
            G.add_node(aisle)

        # Add the rack bays to the graph
        for rack_bay in self.rack_bays:
            G.add_node(rack_bay)

        # Add the viewpoint vertices to the graph (if they aren't already in aisles or rack_bays)
        viewpoints = [vertex for vertex in self.vertices if vertex.params['is_inspection_point']]
        for viewpoint in viewpoints:
            G.add_node(viewpoint)

        # Create Shapely objects for viewpoints and rack bays
        shapely_viewpoints = [viewpoint.to_shapely_point() for viewpoint in viewpoints]
        shapely_rack_bays = [rack_bay.to_shapely_polygon() for rack_bay in self.rack_bays]
        rack_bay_mapping = {rack_bay.to_shapely_polygon(): rack_bay for rack_bay in self.rack_bays}

        # Build STRtree for quick nearest-neighbor query
        tree = STRtree(shapely_rack_bays)

        # Find and add the edges between viewpoints and their closest rack bays
        for viewpoint, shapely_viewpoint in zip(viewpoints, shapely_viewpoints):
            closest_shapely_rack_bay = tree.nearest(shapely_viewpoint)
            closest_rack_bay = rack_bay_mapping[closest_shapely_rack_bay]
            G.add_edge(viewpoint, closest_rack_bay)
            G.add_edge(closest_rack_bay, viewpoint)

        # Add edges between the viewpoints and the aisles that the are in
        for viewpoint in viewpoints:
            for aisle in self.aisles:
                if aisle.contains_vertex(viewpoint):
                    G.add_edge(viewpoint, aisle)
                    G.add_edge(aisle, viewpoint)

        for i, aisle1 in enumerate(self.aisles):
            for aisle2 in self.aisles[i + 1:]:  # To avoid double checking and self-loops
                shared_edge = aisle1.get_shared_edge(aisle2)
                if shared_edge is not None:
                    # Calculate weights based on whether the connecting aisle is a main aisle
                    weight_1_to_2 = MAIN_AISLE_WEIGHT if aisle2.params['is_main_aisle'] else NON_MAIN_AISLE_WEIGHT
                    weight_2_to_1 = MAIN_AISLE_WEIGHT if aisle1.params['is_main_aisle'] else NON_MAIN_AISLE_WEIGHT

                    # Add directed edges with associated weights for traversal towards each aisle
                    G.add_edge(aisle1, aisle2, weight=weight_1_to_2, shared_edge=shared_edge)
                    G.add_edge(aisle2, aisle1, weight=weight_2_to_1, shared_edge=shared_edge)

        # Return the graph
        return G
