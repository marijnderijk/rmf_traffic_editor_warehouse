#!/usr/bin/env python3

import argparse
import yaml
from map.level import Level


def parse_level(level_yaml_path: str, level_name: str):
    with open(level_yaml_path, 'r') as file:
        yaml_data = yaml.safe_load(file).get('levels', {}).get(level_name, {})
    return Level.from_yaml(yaml_data, level_yaml_path)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('level_yaml_path', type=str, help='Path to the level YAML file')
    parser.add_argument('level_name', type=str, help='Name of the level')
    args = parser.parse_args()

    level = parse_level(args.level_yaml_path, args.level_name)
    print(level)

if __name__ == '__main__':
    main()

