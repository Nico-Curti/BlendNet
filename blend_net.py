# -*- coding: utf-8 -*-
"""
Created on Thu Feb  1 15:31:12 2018

@author: nico
"""

import networkx as nx # graph and layout
import pandas as pd # edges dataframe 
import sys # exit
import os # exists file
import argparse # parse command line
import ast # convert string to list
import json # file as json
import numpy as np # append numpy array
import random # nrg
# blender python
import bpy 
from math import acos, degrees, pi
from mathutils import Vector
from matplotlib import colors as mcolors

all_colors = dict(mcolors.BASE_COLORS, **mcolors.CSS4_COLORS)
all_colors = {name : mcolors.to_rgb(ash) for name, ash in all_colors.items()}


def blend_net(graph, position, dim, colors, node_size=3, edge_thickness=0.25, direct=False):
    # edge obj
    bpy.data.materials.new(name="light_gray")
    bpy.data.materials["light_gray"].diffuse_color = (0.4627450980392157, 0.4627450980392157, 0.4627450980392157)
    bpy.data.materials["light_gray"].specular_intensity = 0.5
    # sphere obj
    for color in colors:
        #color = [x / 255.0 for x in name_to_rgb(color)]
        bpy.data.materials.new(name=color)
        bpy.data.materials[color].diffuse_color = all_colors[color]
        bpy.data.materials[color].specular_intensity = 0.5

        # Don't specify more parameters if these colors
        if color == "gray" or color == "light_gray":
            continue

        # Transparency parameters
        bpy.data.materials[color].use_transparency = True
        bpy.data.materials[color].transparency_method = "RAYTRACE"
        bpy.data.materials[color].alpha = 0.1 if color == "clear" else 0.95
        bpy.data.materials[color].raytrace_transparency.fresnel = 0.1
        bpy.data.materials[color].raytrace_transparency.ior = 1.15


    # Set scene, light and alpha_mode
    scene = bpy.context.scene
    scene.render.engine = 'BLENDER_RENDER' # 'CYCLE'
    scene.render.alpha_mode = 'TRANSPARENT' # remove background
    #camera = bpy.context.scene.camera
    #camera.data.type = 'PERSP'
    area = next(area for area in bpy.context.screen.areas if area.type == 'VIEW_3D')
    area.spaces[0].region_3d.view_perspective = 'CAMERA'

    bpy.data.worlds["World"].light_settings.use_ambient_occlusion = True
    bpy.data.worlds["World"].light_settings.samples = 10

    # camera position
    if(len(bpy.data.cameras) == 1):
        obj = bpy.data.objects['Camera'] # bpy.types.Camera
        if dim == 2:
            loc_camera = obj.matrix_world.to_translation()
            mean_x = np.mean([el[0] for el in position.values()])
            mean_y = np.mean([el[1] for el in position.values()])
            obj.location.x = mean_x
            obj.location.y = mean_y

            min_x = min([el[0] for el in position.values()])
            max_x = max([el[0] for el in position.values()])
            min_y = min([el[1] for el in position.values()])
            max_y = max([el[1] for el in position.values()])
            obj.location.z = max(max_x - min_x, max_y - min_y)/(2 * np.tan(np.radians(20)/2))
            obj.rotation_euler = (0.0, 0.0, np.radians(90))
            obj.keyframe_insert(data_path="location", frame=10.0)

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
            obj.location.z = mean_z + max(max_x - min_x, max_y - min_y)/(2 * np.tan(np.radians(20)/2))
            obj.rotation_euler = (0.0, 0.0, np.radians(90))
            obj.keyframe_insert(data_path="location", frame=10.0)

    # Add some mesh primitives
    bpy.ops.object.select_all(action='DESELECT')
    bpy.ops.mesh.primitive_uv_sphere_add()
    sphere = bpy.context.object
    bpy.ops.mesh.primitive_cylinder_add()
    cylinder = bpy.context.object
    cylinder.active_material = bpy.data.materials["light_gray"]
    cone = bpy.context.object
    cone.active_material = bpy.data.materials["light_gray"]
    
    # Keep references to all nodes and edges
    shapes = []
    # Keep separate references to shapes to be smoothed
    shapes_to_smooth = []
    
    # Draw nodes
    nx.set_node_attributes(G, [], "color")
    for node in graph.nodes():
        # Coloring rule for nodes. Edit this to suit your needs!
        col = random.choice(colors)
        
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
        
    # Draw edges
    for source, target in graph.edges():
        # Get source and target locations by drilling down into data structure
        source_loc = position[source]#network["nodes"][edge["source"]]["location"]
        target_loc = position[target]#network["nodes"][edge["target"]]["location"]

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
        edge_cylinder.rotation_mode = "AXIS_ANGLE"
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
            arrow_cone.rotation_mode = "AXIS_ANGLE"
            arrow_cone.rotation_axis_angle = [angle + pi] + list(v_rot)
            bpy.context.scene.objects.link(arrow_cone)
            shapes.append(arrow_cone)
        
    # Remove primitive meshes
    bpy.ops.object.select_all(action='DESELECT')
    sphere.select = True
    cylinder.select = True
    cone.select = True
    
    # If the starting cube is there, remove it
    if "Cube" in bpy.data.objects.keys():
        bpy.data.objects.get("Cube").select = True
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
    bpy.ops.object.origin_set(type="ORIGIN_GEOMETRY", center="MEDIAN")

    # Refresh scene
    bpy.context.scene.update()

if __name__ == "__main__":
    argv = sys.argv
    argv = argv[argv.index("--") + 1:]  # get all args after "--"
    
    description = "BlenderNet"
    parser = argparse.ArgumentParser(description = description)
    parser.add_argument("-f", required=False, dest="filename", action="store", help="filename as networkx dataframe", default="")
    parser.add_argument("-e", required=False, dest="edges", action="store", help="string with edges", default="")
    parser.add_argument("-d", required=False, dest="dim", action="store", help="dimension to plot (2 or 3)", default=3)
    parser.add_argument("-x", required=False, dest="direct", action="store", help="direct/undirect graph", default=False)
    
    if len(sys.argv) <= 1:
        parser.print_help()
        sys.exit(1)
    else:
        args = parser.parse_args(argv)
    
    filename = args.filename
    edges = args.edges
    dim = int(args.dim)
    direct = bool(int(args.direct))
    G = nx.Graph()
    
    if filename != "" and os.path.exists(filename):
        data = pd.read_csv(filename, sep=",", header=0)
        data.columns = [str(c).upper() for c in data.columns]
        edges = data[['SOURCE', 'TARGET']].values
        G.add_edges_from(edges)
        if 'COLORS' in data.columns:
            colors = data['COLORS']
        else:
            colors = np.random.choice(list(all_colors.keys()), size=len(G.nodes))
        is_coords = list(filter(lambda x: x in data.columns, ['X', 'Y']))
        if len(is_coords) != 0:
            if 'Z' in data.columns:
                position = data[['X', 'Y', 'Z']]
            else:
                position = data[['X', 'Y']]
        else:
            position = nx.spring_layout(G, dim=dim, scale=10)
            if dim == 2:
                for key in position.keys():
                    position[key] = np.append(position[key], 0.)

    elif edges == "" and filename == "":
        parser.print_help()
        sys.exit(1)
    else:
        G.add_edges_from(ast.literal_eval(edges))
        position = nx.spring_layout(G, dim=dim, scale=10)
        if dim == 2:
            for key in position.keys():
                position[key] = np.append(position[key], 0.)
        colors = np.random.choice(list(all_colors.keys()), size=len(G.nodes))
        
    blend_net(graph = G, position = position, dim = dim, colors = colors, node_size = 3, edge_thickness = .25, direct = direct )
