[![](https://github.com/osrf/traffic_editor/workflows/ci/badge.svg)](https://github.com/osrf/traffic_editor/actions/workflows/ci.yaml)
[![](https://github.com/osrf/traffic_editor/workflows/pycodestyle/badge.svg)](https://github.com/osrf/traffic_editor/actions/workflows/pycodestyle.yaml)

# rmf_traffic\_editor: warehouse edition

Hi there. This is my fork of the rmf_traffic_editor, a gui tool for creating floorplans and traffic patterns for the [RMF Project](https://github.com/open-rmf).
This fork extends the original traffic editor to support warehouse specific features such as:
- storage racks
- aisles
- rack inspection waypoints

![](docs/rmf_traffic_editor_warehouse_gui.png)

My work was done in the following directories:
 * `rmf_traffic_editor`: C++-based GUI for creating floorplans. I extended the original traffic editor with warehouse-specific features.
 * `planning_tools`: Python based tools for creating routes within the generated warehouse floorplans.


The original repository also contains useful tools which have not yet been extended with the warehouse-specific features, but this could be done at a later stage:
 * `rmf_building_map_tools`: Python-based tools to use and manipulate the map files created by `rmf_traffic_editor`, such as:
   * `building_map_server`:  a ROS 2 node to serve maps using `rmf_building_map_msgs`
   * translators to simulators such as Gazebo
   * translators to navigation packages such as `rmf_core` (e.g. `rmf_ros2`)
   * scripts that handle downloading of gazebo models. `pit_crew`, `building_map_model_downloader`...
 * `rmf_traffic_editor_assets`: Gazebo model thumbnails, in used by `traffic_editor` GUI

---

## Installation

This repository is structured as a collection of ROS 2 packages and can be built using `colcon`.
For full installation of RMF, please refer to [here](https://github.com/open-rmf/rmf).

The `rmf_building_map_tools` package requires the following Python 3 dependencies to generate worlds:

```
sudo apt install python3-shapely python3-yaml python3-requests
```

## Usage

### Traffic Editor GUI

Instructions for using the `traffic_editor` are located [here](https://osrf.github.io/ros2multirobotbook/traffic-editor.html)

To run traffic_editor GUI, run:
```bash
source install/setup.bash
traffic-editor
```





