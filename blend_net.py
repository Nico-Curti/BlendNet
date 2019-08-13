#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division
from __future__ import print_function

import os              # exists file
import sys             # exit
import ast             # convert string to list
import argparse        # parse command line
import numpy as np     # append numpy array
import pandas as pd    # edges dataframe
import networkx as nx  # graph and layout

# blender python

import bpy
from math import acos, pi
from mathutils import Vector
from matplotlib import colors as mcolors

__package__ = 'Blender Network viewer'
__author__  = ['Nico Curti']
__email__   = ['nico.curti2@unibo.it']

all_colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
all_colors = {name : mcolors.to_rgb(ash) for name, ash in all_colors.items()}


def blend_net (graph, node_size=3.0, edge_thickness=0.25, direct=False):
  '''
  Blender Network viewer

  Parameters
  ----------
    graph : networkx graph
      Graph object to view. If graph nodes must have 'position' and 'colors' attributes. It it has also
      the 'names' attribute it will be used for label.

    node_size : float
      Size of the node in the rendering.

    edge_thickness : float
      Size of the edges in the rendering

    direct : bool
      Switch between direct or bidirection edges in the graph

  Returns
  -------
    Blender interface

  Notes
  -----
  This function can be called ONLY by the Python of Blender software. Thus Blender should be installed and
  at the end the Blender interface is opened with the graph visualization.
  Move the camera and render the graph.
  It could be useful to set the camera to the selected view and then render the picture.
  '''

  # edge obj
  bpy.data.materials.new(name='light_gray')
  bpy.data.materials['light_gray'].diffuse_color = (0.4627450980392157, 0.4627450980392157, 0.4627450980392157)
  bpy.data.materials['light_gray'].specular_intensity = 0.5

  # sphere obj
  colors = nx.get_node_attributes(graph, 'colors')
  for _, color in colors.items():
    bpy.data.materials.new(name=color)
    bpy.data.materials[color].diffuse_color = all_colors[color]
    bpy.data.materials[color].specular_intensity = 0.5

    # Don't specify more parameters if these colors
    if color == "gray" or color == 'light_gray':
      continue

    # Transparency parameters
    bpy.data.materials[color].use_transparency = True
    bpy.data.materials[color].transparency_method = 'RAYTRACE'
    bpy.data.materials[color].alpha = 0.1 if color == 'clear' else 0.95
    bpy.data.materials[color].raytrace_transparency.fresnel = 0.1
    bpy.data.materials[color].raytrace_transparency.ior = 1.15

  # text obj
  text = bpy.data.objects.new('label', bpy.data.curves.new(type='FONT', name='curve'))
  bpy.data.materials.new(name='black')
  bpy.data.materials['black'].diffuse_color = (0, 0, 0)
  bpy.data.materials['black'].specular_intensity = 0.5

  # Set scene, light and alpha_mode
  scene = bpy.context.scene
  scene.render.engine = 'BLENDER_RENDER' # 'CYCLE'
  scene.render.alpha_mode = 'TRANSPARENT' # remove background

  area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
  area.spaces[0].region_3d.view_perspective = 'CAMERA'

  bpy.data.worlds['World'].light_settings.use_ambient_occlusion = True
  bpy.data.worlds['World'].light_settings.samples = 10

  # camera position

  position = nx.get_node_attributes(G, 'position')
  z = [v[-1] for v in position.values()]

  dim = 2 if np.allclose(z, np.zeros(shape=len(z))) else 3

  if (len(bpy.data.cameras) == 1):
    obj = bpy.data.objects['Camera'] # bpy.types.Camera

    if dim == 2:

      loc_camera = obj.matrix_world.to_translation()
      mean_x = np.mean([el[0] for el in position.values()])
      mean_y = np.mean([el[1] for el in position.values()])
      mean_z = 0.
      obj.location.x = mean_x
      obj.location.y = mean_y

      min_x = min([el[0] for el in position.values()])
      max_x = max([el[0] for el in position.values()])
      min_y = min([el[1] for el in position.values()])
      max_y = max([el[1] for el in position.values()])
      obj.location.z = max(max_x - min_x, max_y - min_y)/(2 * np.tan(np.radians(20)/2))
      obj.rotation_euler = (0.0, 0.0, np.radians(90))
      obj.keyframe_insert(data_path='location', frame=10.0)

    elif dim == 3:

      mean_x = np.mean([el[0] for el in position.values()])
      mean_y = np.mean([el[1] for el in position.values()])
      mean_z = np.mean([el[2] for el in position.values()])

      obj.location.x = mean_x
      obj.location.y = mean_y
      min_x = min([el[0] for el in position.values()])
      max_x = max([el[0] for el in position.values()])
      min_y = min([el[1] for el in position.values()])
      max_y = max([el[1] for el in position.values()])
      obj.location.z = mean_z + max(max_x - min_x, max_y - min_y)/(2 * np.tan(np.radians(20) * .5))
      obj.rotation_euler = (0.0, 0.0, np.radians(90))
      obj.keyframe_insert(data_path="location", frame=10.0)

  # Add some mesh primitives
  bpy.ops.object.select_all(action='DESELECT')
  bpy.ops.mesh.primitive_uv_sphere_add()
  sphere = bpy.context.object
  bpy.ops.mesh.primitive_cylinder_add()
  cylinder = bpy.context.object
  cylinder.active_material = bpy.data.materials['light_gray']
  bpy.ops.mesh.primitive_cone_add()
  cone = bpy.context.object
  cone.active_material = bpy.data.materials['light_gray']

  # Keep references to all nodes and edges
  shapes = []
  # Keep separate references to shapes to be smoothed
  shapes_to_smooth = []

  # Draw nodes
  label = nx.get_node_attributes(graph, 'names')

  for node in graph.nodes():
    # Coloring rule for nodes. Edit this to suit your needs!
    col = colors[node]

    # Copy mesh primitive and edit to make node
    # (You can change the shape of drawn nodes here)
    node_sphere = sphere.copy()
    node_sphere.data = sphere.data.copy()
    node_sphere.location = position[node]
    node_sphere.dimensions = [node_size] * 3
    node_sphere.active_material = bpy.data.materials[col]
    bpy.context.scene.objects.link(node_sphere)
    shapes.append(node_sphere)
    shapes_to_smooth.append(node_sphere)

    if label:
      lbl = text.copy()
      lbl.data = text.data.copy()
      lbl.data.body = label[node]
      lbl.rotation_mode = 'AXIS_ANGLE'
      lbl.rotation_euler = (0.0, 0.0, np.radians(90))
      lbl.active_material = bpy.data.materials['black']
      lbl.location = position[node] + [0., 0., node_size * .5]
      bpy.context.scene.objects.link(lbl)

  # Draw edges
  for source, target in graph.edges():
    # Get source and target locations by drilling down into data structure
    source_loc = position[source]
    target_loc = position[target]

    diff = [c2 - c1 for c2, c1 in zip(source_loc, target_loc)]
    cent = [(c2 + c1) / 2 for c2, c1 in zip(source_loc, target_loc)]
    mag = sum([(c2 - c1) ** 2 for c1, c2 in zip(source_loc, target_loc)]) ** 0.5

    # Euler rotation calculation
    v_axis = Vector(diff).normalized()
    v_obj = Vector((0, 0, 1))
    v_rot = v_obj.cross(v_axis)
    angle = acos(v_obj.dot(v_axis))

    # Copy mesh primitive to create edge
    edge_cylinder = cylinder.copy()
    edge_cylinder.data = cylinder.data.copy()
    edge_cylinder.dimensions = [edge_thickness] * 2 + [mag - node_size]
    edge_cylinder.location = cent
    edge_cylinder.rotation_mode = 'AXIS_ANGLE'
    edge_cylinder.rotation_axis_angle = [angle] + list(v_rot)
    bpy.context.scene.objects.link(edge_cylinder)
    shapes.append(edge_cylinder)
    shapes_to_smooth.append(edge_cylinder)

    # Copy another mesh primitive to make an arrow head
    if direct:

      arrow_cone = cone.copy()
      arrow_cone.data = cone.data.copy()
      arrow_cone.dimensions = [edge_thickness * 4.0] * 3
      arrow_cone.location = cent
      arrow_cone.rotation_mode = 'AXIS_ANGLE'
      arrow_cone.rotation_axis_angle = [angle + pi] + list(v_rot)
      bpy.context.scene.objects.link(arrow_cone)
      shapes.append(arrow_cone)

  # Remove primitive meshes
  bpy.ops.object.select_all(action='DESELECT')
  sphere.select = True
  cylinder.select = True
  cone.select = True

  # If the starting cube is there, remove it
  if 'Cube' in bpy.data.objects.keys():
    bpy.data.objects.get('Cube').select = True
  bpy.ops.object.delete()

  # Smooth specified shapes
  for shape in shapes_to_smooth:
    shape.select = True
  bpy.context.scene.objects.active = shapes_to_smooth[0]
  bpy.ops.object.shade_smooth()

  # Join shapes
  for shape in shapes:
    shape.select = True
  bpy.context.scene.objects.active = shapes[0]
  bpy.ops.object.join()

  # Center object origin to geometry
  bpy.ops.object.origin_set(type='ORIGIN_GEOMETRY', center='MEDIAN')

  # Refresh scene
  bpy.context.scene.update()




if __name__ == "__main__":

  argv = sys.argv
  argv = argv[argv.index("--") + 1:]  # get all args after "--"

  description = 'BlenderNet'
  parser = argparse.ArgumentParser(description=description)

  parser.add_argument('-E', required=False, type=str, dest='edgelist', action='store', help='edgelist filename as networkx dataframe', default='')
  parser.add_argument('-N', required=False, type=str, dest='nodelist', action='store', help='nodelist filename as networkx dataframe', default='')
  parser.add_argument('-e', required=False, type=str, dest='edges', action='store', help='string with edges', default='')
  parser.add_argument('-n', required=False, type=str, dest='nodes', action='store', help='string with nodes', default='')
  parser.add_argument('-d', required=False, type=int, dest='dim', action='store', help='dimension to plot', choices=[2, 3], default=3)
  parser.add_argument('-x', required=False, type=int, dest="direct", action="store", help='direct/undirect graph', default=False)
  parser.add_argument('-s', required=False, type=float, dest="nsize", action="store", help='node size', default=3)
  parser.add_argument('-l', required=False, type=float, dest="esize", action="store", help='edge thickness', default=.25)

  if len(sys.argv) <= 1:

    parser.print_help()
    raise ValueError('Incorrenct number of input given')

  else:

    args = parser.parse_args(argv)

  G = nx.Graph()

  if args.edgelist != '' and not os.path.exists(args.edgelist):
    parser.print_help()
    raise FileNotFoundError('Incorrenct number of input given. Edgelist filename not found. Given {}'.format(args.edgelist))

  if args.nodelist != '' and not os.path.exists(args.nodelist):
    parser.print_help()
    raise FileNotFoundError('Incorrenct number of input given. Nodelist filename not found. Given {}'.format(args.nodelist))

  cases = [args.edges != '', args.edgelist != '', args.nodes != '', args.nodelist != ''] # cases input array

  if np.all(cases == [1, 0, 0, 0]): # edges as string found

    G.add_edges_from(ast.literal_eval(args.edges))

    position = nx.spring_layout(G, dim=args.dim, scale=10)

    if args.dim == 2:
      position = {k : (x, y, 0.) for k, (x, y) in position.items()}

    colors = np.random.choice(all_colors.keys(), size=len(G.nodes))
    colors = {k : v for k, v in zip(G.nodes, colors)}

    nx.set_node_attributes(G, position, 'position')
    nx.set_node_attributes(G, colors, 'colors')


  elif np.all(cases == [0, 0, 1, 0]): # nodes as string found

    G.add_nodes_from(ast.literal_eval(args.nodes))

    position = nx.spring_layout(G, dim=args.dim, scale=10)

    if args.dim == 2:
      position = {k : (x, y, 0.) for k, (x, y) in position.items()}

    colors = np.random.choice(all_colors.keys(), size=len(G.nodes))
    colors = {k : v for k, v in zip(G.nodes, colors)}

    nx.set_node_attributes(G, position, 'position')
    nx.set_node_attributes(G, colors, 'colors')


  elif np.all(cases == [1, 0, 1, 0]): # edges as string AND nodes as string found

    G.add_nodes_from(ast.literal_eval(args.nodes))
    G.add_edges_from(ast.literal_eval(args.edges))

    position = nx.spring_layout(G, dim=args.dim, scale=10)

    if args.dim == 2:
      position = {k : (x, y, 0.) for k, (x, y) in position.items()}

    colors = np.random.choice(all_colors.keys(), size=len(G.nodes))
    colors = {k : v for k, v in zip(G.nodes, colors)}

    nx.set_node_attributes(G, position, 'position')
    nx.set_node_attributes(G, colors, 'colors')


  elif np.all(cases == [0, 1, 0, 0]): # edges as file found

    edges = pd.read_csv(args.edgelist, sep=',', header=0)

    edges.columns = [str(c).upper() for c in edges.columns]

    edges = edges[['SOURCE', 'TARGET']].values
    G.add_edges_from(edges)

    position = nx.spring_layout(G, dim=args.dim, scale=10)

    if args.dim == 2:
      position = {k : (x, y, 0.) for k, (x, y) in position.items()}

    colors = np.random.choice(all_colors.keys(), size=len(G.nodes))
    colors = {k : v for k, v in zip(G.nodes, colors)}

    nx.set_node_attributes(G, position, 'position')
    nx.set_node_attributes(G, colors, 'colors')


  elif np.all(cases == [0, 0, 0, 1]): # nodes as file found

    nodes = pd.read_csv(args.nodelist, sep=',', header=0)

    nodes.columns = [str(c).upper() for c in nodes.columns]

    node = nodes['NODE'].values
    G.add_nodes_from(node)

    if 'COLORS' in nodes.columns:
      colors = {k : v for k, v in nodes['COLORS'].items()}

      nx.set_node_attributes(G, colors, 'colors')

    else:

      colors = np.random.choice(all_colors.keys(), size=len(nodes))
      colors = {k : v for k, v in zip(G.nodes, colors)}

      nx.set_node_attributes(G, colors, 'colors')

    if 'NAMES' in nodes.columns:
      names = {k : v for k, v in nodes['NAMES'].items()}
      nx.set_node_attributes(G, names, 'names')

    is_coords = list(filter(lambda x: x in nodes.columns, ['X', 'Y']))

    if len(is_coords) != 0:
      if 'Z' in nodes.columns:
        position = {n : (x, y, z) for n, (x, y, z) in nodes[['X', 'Y', 'Z']].iterrows()}
      else:
        position = {n : (x, y, 0.) for n, (x, y) in nodes[['X', 'Y']].iterrows()}

      nx.set_node_attributes(G, position, 'position')

    else:

      position = nx.spring_layout(G, dim=args.dim, scale=10)

      if args.dim == 2:
        position = {k : (x, y, 0.) for k, (x, y) in position.items()}

      nx.set_node_attributes(G, position, 'position')


  elif np.all(cases == [0, 1, 0, 1]): # edges as file AND nodes as file found

    edges = pd.read_csv(args.edgelist, sep=',', header=0)

    edges.columns = [str(c).upper() for c in edges.columns]

    edges = edges[['SOURCE', 'TARGET']].values
    G.add_edges_from(edges)

    nodes = pd.read_csv(args.nodelist, sep=',', header=0)
    nodes.columns = [str(c).upper() for c in nodes.columns]


    if 'NODE' in nodes.columns:
      node = nodes['NODE'].values
      G.add_nodes_from(node)

    if 'COLORS' in nodes.columns:
      colors = {k : v for k, v in nodes['COLORS'].items()}
      nx.set_node_attributes(G, colors, 'colors')

    else:
      colors = np.random.choice(all_colors.keys(), size=len(nodes))
      colors = {k : v for k, v in zip(G.nodes, colors)}

      nx.set_node_attributes(G, colors, 'colors')

    if 'NAMES' in nodes.columns:
      names = {k : v for k, v in nodes['NAMES'].items()}
      nx.set_node_attributes(G, names, 'names')

    is_coords = list(filter(lambda x: x in nodes.columns, ['X', 'Y']))

    if len(is_coords) != 0:

      if 'Z' in nodes.columns:
        position = {n : (x, y, z) for n, (x, y, z) in nodes[['X', 'Y', 'Z']].iterrows()}
      else:
        position = {n : (x, y, 0.) for n, (x, y) in nodes[['X', 'Y']].iterrows()}

      nx.set_node_attributes(G, position, 'position')

    else:
      position = nx.spring_layout(G, dim=args.dim, scale=10)

      if args.dim == 2:
        position = {k : (x, y, 0.) for k, (x, y) in position.items()}

      nx.set_node_attributes(G, position, 'position')


  else:

    parser.print_help()
    raise ValueError('Incorrenct number of input given')

  blend_net(graph=G,
            node_size=args.nsize,
            edge_thickness=args.esize,
            direct=args.direct
            )

