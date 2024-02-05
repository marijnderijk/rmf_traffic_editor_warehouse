#!/usr/bin/env python3

import argparse
import yaml
from map.level import Level
from utils.draw_graph import draw_graph
from utils.draw_graph_geometry import draw_graph_geometry
from utils.compute_shortest_path import compute_shortest_path


def parse_level(level_yaml_path: str, level_name: str):
    with open(level_yaml_path, 'r') as file:
        yaml_content = yaml.safe_load(file)
    levels = yaml_content.get('levels', {})
    if level_name not in levels:
        raise ValueError(f"Level '{level_name}' not found in {level_yaml_path}.")
    yaml_data = levels[level_name]
    return Level.from_yaml(yaml_data, level_yaml_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('level_yaml_path', type=str, help='Path to the level YAML file')
    parser.add_argument('level_name', type=str, help='Name of the level')
    args = parser.parse_args()

    level = parse_level(args.level_yaml_path, args.level_name)
    level.set_polygon_vertices()

    network = level.create_network()

    # ask for the source and target names
    available_nodes = [node.name for node in network.nodes]
    print(f"Available nodes: {available_nodes}")
    # source_name = input("Enter the source node name: ")
    # target_name = input("Enter the target node name: ")
    source_name = "rack_mini_1_viewpoint_0_9"
    target_name = "conveyor_rack_2_viewpoint_2_0"

    shortest_path = compute_shortest_path(network, source_name, target_name)

    draw_graph(network, shortest_path)

    draw_graph_geometry(network, shortest_path=shortest_path)

if __name__ == '__main__':
    main()
