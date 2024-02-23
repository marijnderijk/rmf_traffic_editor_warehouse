import matplotlib.pyplot as plt
import geopandas as gpd
import networkx as nx


def draw_graph_geometry(
    G: nx.Graph, base_alpha=0.5, highlight_alpha=0.8, shortest_path: list = []
):
    point_shapes = []
    sp_point_shapes = []
    polygon_shapes = []
    sp_polygon_shapes = []
    transition_lines = []
    sp_transition_lines = []

    for node in G.nodes:
        shapely_shape = node.shapely()
        if shapely_shape.geom_type == "Point":
            if node in shortest_path:
                sp_point_shapes.append(shapely_shape)
            else:
                point_shapes.append(shapely_shape)
        elif shapely_shape.geom_type == "Polygon":
            if node in shortest_path:
                sp_polygon_shapes.append(shapely_shape)
            else:
                polygon_shapes.append(shapely_shape)

    for u, v, d in G.edges(data=True):
        if "shared_edge" in d:
            transition_lines.append(d["shared_edge"])

    if shortest_path:
        path_edges = list(zip(shortest_path, shortest_path[1:]))
        sp_transition_lines = [
            G[u][v]["shared_edge"] for u, v in path_edges if "shared_edge" in G[u][v]
        ]

    polygon_gdf = gpd.GeoSeries(polygon_shapes)
    point_gdf = gpd.GeoSeries(point_shapes)
    line_gdf = gpd.GeoSeries(transition_lines)

    if shortest_path:
        sp_line_gdf = gpd.GeoSeries(sp_transition_lines)
        sp_point_gdf = gpd.GeoSeries(sp_point_shapes)
        sp_polygon_gdf = gpd.GeoSeries(sp_polygon_shapes)

    # make sure points are on top of lines
    polygon_gdf.plot(ax=plt.gca(), color="lightgrey", alpha=base_alpha)
    point_gdf.plot(ax=plt.gca(), color="black", alpha=base_alpha, markersize=5)
    line_gdf.plot(ax=plt.gca(), color="yellow", alpha=base_alpha)

    if shortest_path:
        sp_polygon_gdf.plot(ax=plt.gca(), color="orange", alpha=highlight_alpha)
        sp_point_gdf.plot(ax=plt.gca(), color="red", alpha=highlight_alpha, markersize=5)
        sp_line_gdf.plot(ax=plt.gca(), color="red", alpha=highlight_alpha)

    plt.gca().invert_yaxis()

    plt.show()



