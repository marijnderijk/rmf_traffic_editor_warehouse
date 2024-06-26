/*
 * Copyright (C) 2019-2021 Open Source Robotics Foundation
 *
 * Licensed under the Apache License, Version 2.0 (the "License");
 * you may not use this file except in compliance with the License.
 * You may obtain a copy of the License at
 *
 *     http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software
 * distributed under the License is distributed on an "AS IS" BASIS,
 * WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
 * See the License for the specific language governing permissions and
 * limitations under the License.
 *
 */

#include "polygon.h"
using std::string;
using std::vector;

Polygon::Polygon() { create_required_parameters(); }

Polygon::~Polygon() {}

void Polygon::from_yaml(const YAML::Node &data, const Type polygon_type) {
  if (!data.IsMap())
    throw std::runtime_error("Polygon::from_yaml() expected a map");
  type = polygon_type;
  for (YAML::const_iterator it = data["vertices"].begin();
       it != data["vertices"].end(); ++it) {
    vertices.push_back(it->as<int>());
  }

  // load the parameters
  if (data["parameters"]) {
    for (YAML::const_iterator it = data["parameters"].begin();
         it != data["parameters"].end(); ++it) {
      Param p;
      p.from_yaml(it->second);
      params[it->first.as<string>()] = p;
    }
  }

  create_required_parameters();
}

YAML::Node Polygon::to_yaml() const {
  YAML::Node y;
  for (const auto &vertex_idx : vertices)
    y["vertices"].push_back(vertex_idx);
  y["vertices"].SetStyle(YAML::EmitterStyle::Flow);
  y["parameters"] = YAML::Node(YAML::NodeType::Map);
  for (const auto &param : params)
    y["parameters"][param.first] = param.second.to_yaml();
  y["parameters"].SetStyle(YAML::EmitterStyle::Flow);
  return y;
}

void Polygon::remove_vertex(const int vertex_idx) {
  // find first occurrence of this vertex_idx
  int vertex_occurrence_idx = -1;
  for (int i = 0; i < static_cast<int>(vertices.size()); i++) {
    if (vertices[i] == vertex_idx) {
      vertex_occurrence_idx = i;
      break;
    }
  }
  if (vertex_occurrence_idx < 0) {
    printf("never found vertex %d\n", vertex_idx);
    return; // never found it. so sad.
  }
  printf("found vertex %d at polygon vertices idx %d\n", vertex_idx,
         vertex_occurrence_idx);

  vertices.erase(vertices.begin() + vertex_occurrence_idx);

  // not sure what's going on here, but it doesn't work :(
  // vector<int> &v = vertices;  // save typing
  // v.erase(std::remove(v.begin(), v.end(), vertex_idx), v.end());
}

void Polygon::set_param(const std::string &name, const std::string &value) {
  auto it = params.find(name);
  if (it == params.end()) {
    printf("tried to set unknown parameter [%s]\n", name.c_str());
    return; // unknown parameter
  }
   it->second.set(value);
}

void Polygon::create_required_parameters() {
  // create required parameters if they don't exist yet on this edge
  if (type == FLOOR) {
    create_param_if_needed("texture_name", Param::STRING,
                           std::string("blue_linoleum"));
    create_param_if_needed("texture_scale", Param::DOUBLE, 1.0);
    create_param_if_needed("texture_rotation", Param::DOUBLE, 0.0);
    create_param_if_needed("indoor", Param::INT, 0);
    create_param_if_needed("ceiling_texture", Param::STRING,
                           std::string("blue_linoleum"));
    create_param_if_needed("ceiling_scale", Param::DOUBLE, 1.0);
  }

  if (type == STORAGE_RACK) {
    create_param_if_needed("name", Param::STRING, std::string("rack"));
    create_param_if_needed("num_bays", Param::INT,
                           4); // number of bays (lenghtwise)
    create_param_if_needed("num_rows", Param::INT, 2); // number of rows
    create_param_if_needed("viewpoint_distance", Param::DOUBLE, 3.0);
    create_param_if_needed("units_per_bay", Param::INT,
                           4); // number of units per bay
    // now we want to create a height parameter for each unit
    int units_per_bay = params["units_per_bay"].to_qstring().toInt();
    for (int i = 0; i < units_per_bay; i++) {
      char param_name[64];
      sprintf(param_name, "unit_height_%d", i);
      create_param_if_needed(param_name, Param::DOUBLE, 0.5);
    }
    // if there are extra unit heights, remove them
    for (int i = units_per_bay; i < 10; i++) {
      char param_name[64];
      sprintf(param_name, "unit_height_%d", i);
      params.erase(param_name);
    }
  }

  if (type == RACK_BAY) {
    create_param_if_needed("name", Param::STRING, std::string("bay"));
    create_param_if_needed("parent_rack_name", Param::STRING, std::string(""));
    create_param_if_needed("row", Param::INT, 0);
    create_param_if_needed("number", Param::INT, 0);
    create_param_if_needed("n_units", Param::INT, 4);
    int units_per_bay = params["n_units"].to_qstring().toInt();
    for (int i = 0; i < units_per_bay; i++) {
      char param_name[64];
      sprintf(param_name, "unit_height_%d", i);
      create_param_if_needed(param_name, Param::DOUBLE, 0.5);
    }
    // if there are extra unit heights, remove them
    for (int i = units_per_bay; i < 10; i++) {
      char param_name[64];
      sprintf(param_name, "unit_height_%d", i);
      params.erase(param_name);
    }
  }

  if (type == AISLE) {
    create_param_if_needed("name", Param::STRING, std::string("aisle"));
    create_param_if_needed("main_aisle", Param::BOOL, false);
  }
}

template <typename T>
void Polygon::create_param_if_needed(const std::string &name,
                                     const Param::Type &param_type,
                                     const T &param_value) {
  auto it = params.find(name);
  if (it == params.end() || it->second.type != param_type)
    params[name] = param_value;
    }
